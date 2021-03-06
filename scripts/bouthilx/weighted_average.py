import numpy as np
import argparse
from scipy import io as sio

# Order of the modelFiles
# Activity      - numpy or txt 
# Audio         - numpy
# Bag of mouth  - numpy
# ConvNet       - matlab probs must be under ['prob_values']
# ConvNet+Audio - matlab probs must be under ['prob_values']
# The function automatically adapts to numpy or matlab,
# files names must have .npy, .txt or .mat extension

mat_orders = [[5,6,0,4,1,3,2],
              #[2,4,6,5,3,0,1],
              [0,1,2,3,5,6,4]]
              #[0,1,2,3,6,4,5]]

def load_preds(path):
    if path.split(".")[-1]=="npy":
        preds = np.load(path)
        if np.prod(preds.shape) == 7:
            preds = preds.reshape(1,7)
        return preds
    elif path.split(".")[-1]=="mat":
        preds = sio.loadmat(path)['prob_values_test']
        if np.prod(preds.shape) == 7:
            preds = preds.reshape(1,7)
        return preds
    elif path.split(".")[-1]=="txt":
        txt_file = open(path,'r')
        preds = []
        for line in txt_file.readlines():
            # The 7 probabilities should be at the end of the line
            preds.append([float(prob) for prob in line.strip().split()[-7:]])
        return np.array(preds)
    else:
        raise ValueError("The file must be .npy (numpy), .txt or .mat (matlab)")

def make_weighted_prediction(weightFile, *modelFiles):
    weights = np.load(weightFile)
    model_preds = []
    for i, path in enumerate(modelFiles):
        preds = load_preds(path)
        if path.split(".")[-1]=="mat":
            preds = preds[:,mat_orders[i-3]]
        model_preds.append(preds)

    print model_preds
    preds = np.zeros(model_preds[i].shape)
    for i in xrange(len(model_preds)):
        print model_preds[i]
        preds += weights[i]*model_preds[i]

    print preds
    return preds

def main():
    parser = argparse.ArgumentParser(prog="WEIGHTED_AVERAGE",usage="%(prog)s Weights Activity Audio BagOfMouth ConvNet ConNet+Audio OUTPUT_FILE")
    parser.add_argument("files",nargs=7,help="There should be Weights Activity Audio BagOfMouth ConvNet ConNet+Audio Output files in this exact order")
    options = parser.parse_args()

    files = options.files
    output = make_weighted_prediction(*files[:-1])
    np.save(files[-1],output)

if __name__=="__main__":
    main()
