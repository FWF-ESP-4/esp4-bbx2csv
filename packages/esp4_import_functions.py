import numpy
from numpy import fromfile, zeros, mean, shape, flip
import os
from IPython.display import clear_output


#DEFINING FUNCTIONS
# the authot of the BBXimportNorm function is Johannes Förster (Max Planck Institute for Intelligent Systems, Stuttgart, Germany)
def BBXimportNorm(M, path): #exporting dynamic magnetic contrast
    def BBXimportNorm(M, path):
        """
        Imports and normalizes dynamic magnetic contrast data from a binary file.
        Parameters
        ----------
        M : int
            A multiplier used in the indexing of the third dimension of the output array.
        path : str
            Path to the binary file containing the data.
        Returns
        -------
        Normbild : numpy.ndarray
            A 3D array of shape (Y, X, N) containing the normalized and vertically flipped images.
        N : int
            The number of images (frames) in the dataset.
        Notes
        -----
        - The binary file is expected to contain data in big-endian unsigned 32-bit integer format.
        - The first three values in the file represent the number of images (N), the number of columns (X), and the number of rows (Y), respectively.
        - Each image is normalized by the mean across the third dimension and then vertically flipped.
        """
    with open(path, 'rb') as f:    
        a = fromfile(f, dtype = '>u4')   
    N = a[0]
    Y = a[2]
    X = a[1]
    Bild = zeros([Y, X, N])
    for k in range(0, N): 
        for i in range(0, Y):
            for j in range(0, X):
                Bild[i, j, k * M % N]=a[3 + i + Y * j + Y * X * k]
    
    Normbild = zeros(shape(Bild))
    S = mean(Bild, axis=2)
    for i in range(0, N):
        Normbild[:, :, i] = flip(Bild[:, :, i] / S, axis = 0)
    del(Bild)
    return Normbild, N
    

def BBXimport(M, path): #exporting the chemical contrast
    def BBXimport(M, path):
        """
        Imports and processes chemical contrast data from a binary file.
        This function reads a binary file containing image data, reshapes it into a 3D array,
        normalizes the images by flipping them along the vertical axis, and returns the processed
        image stack along with the number of images.
        Parameters
        ----------
        M : int
            A parameter used in the calculation of the image index during reshaping.
        path : str
            The file path to the binary data file to be imported.
        Returns
        -------
        Normbild : numpy.ndarray
            A 3D numpy array of shape (Y, X, N) containing the normalized (flipped) images.
        N : int
            The number of images (slices) in the stack.
        Notes
        -----
        - The binary file is expected to contain data in big-endian unsigned 32-bit integer format.
        - The first three values in the file specify the number of images (N), the width (X), and the height (Y).
        - The function flips each image vertically.
        """
    with open(path, 'rb') as f:    
        a = fromfile(f, dtype = '>u4')   
    N = a[0]
    Y = a[2]
    X = a[1]
    Bild = zeros([Y, X, N])
    for k in range(0, N): 
        for i in range(0, Y):
            for j in range(0, X):
                Bild[i, j, k * M % N] = a[3 + i + Y * j + Y * X * k]
    
    Normbild = zeros(shape(Bild))
    S = mean(Bild, axis=2)
    for i in range(0, N):
        Normbild[:, :, i] = flip(Bild[:, :, i], axis = 0)
    del(Bild)
    return Normbild, N


def BBX2CSV(path, choice = "magnetic"):
    """
    Converts all .bbx files in the specified directory to CSV files, processing the data in either 'chemical' or 'magnetic' mode.
    Parameters:
        path (str): The directory path containing .bbx files to process.
        choice (str, optional): The processing mode. 
            - 'chemical': Exports raw data.
            - 'magnetic' (default): Exports data normalized by the mean across the third dimension.
    Workflow:
        - Iterates over all .bbx files in the given directory.
        - Imports data from each .bbx file using BBXimport.
        - Processes the data:
            - In 'chemical' mode, exports the raw data.
            - In 'magnetic' mode, normalizes each value by the mean across the third dimension.
        - Writes the processed data to separate CSV files for each slice along the third dimension.
    Output:
        For each .bbx file, creates one CSV file per slice (third dimension) in the same directory.
        The output filenames are suffixed with the slice index and, for chemical mode, an additional marker.
    Notes:
        - Requires the functions BBXimport, zeros, shape, and clear_output to be defined/imported elsewhere.
        - Prints progress and status messages to the console.
    """
    print(choice)

    # Process all .bbx files in the specified path
    for file in os.listdir(path):
        if file.endswith(".bbx"):
            print(file)
            # Import BBX file data
            a = BBXimport(125, path + file)
            # Initialize data array with zeros, shape based on imported data
            data = zeros(shape(a[0]))

            # Iterate through the data array and process each value
            for i in range(0, len(a[0])):
                for j in range(0, len(a[0][i])):
                    for k in range(0, a[1]):
                        if choice == 'chemical':
                            # Mode 1: Use raw data
                            y = a[0][i][j][k]
                        else:
                            # Mode 2: Calculate magnetic contrast
                            y = a[0][i][j][k] / (sum(a[0][i][j]) / a[1])

                        data[i, j, k] = y

            print(y)

            # Write processed data to CSV files, one for each k
            for k in range(0, a[1]):
                clear_output(wait=True)
                print(k+1, '/', a[1])
                if choice == 'chemical':
                    print(choice)
                    # Save chemical mode data
                    with open(path + file[:-4] + "_%d (2).csv" % k, 'w+') as f:
                        for i in range(0, len(data)):
                            for j in range(0, len(data[i])):
                                f.write(str(data[i, j, k]) + ',')
                            f.write('\n')
                else:
                    print(choice)
                    # Save magnetic mode data
                    with open(path + file[:-4] + "_%d.csv" % k, 'w+') as f:
                        for i in range(0, len(data)):
                            for j in range(0, len(data[i])):
                                f.write(str(data[i, j, k]) + ',')
                            f.write('\n')
                    f.close()

    print("Done with " + path)