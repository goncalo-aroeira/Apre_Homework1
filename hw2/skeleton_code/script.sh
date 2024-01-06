python hw2-q2.py -epochs 15 -learning_rate 0.1 -optimizer sgd -no_maxpool 
echo "FINISHED FOR LEARNING RATE 0.1"
python hw2-q2.py -epochs 15 -learning_rate 0.01 -optimizer sgd -no_maxpool 
echo "FINISHED MLP FOR LEARNING RATE 0.01"
python hw2-q2.py -epochs 15 -learning_rate 0.001 -optimizer sgd -no_maxpool
echo "FINISHED MLP FOR LEARNING RATE 0.001"


