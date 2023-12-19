time python3 hw1-q2.py mlp -epochs 20 -batch_size 16 -learning_rate 0.1 -layers 2 -l2_decay 0 -hidden_size 200 -dropout 0.0 -activation relu -optimizer sgd
echo "FINISHED MLP FOR BATCH SIZE 16"
time python3 hw1-q2.py mlp -epochs 20 -batch_size 1024 -learning_rate 0.1 -layers 2 -l2_decay 0 -hidden_size 200 -dropout 0.0 -activation relu -optimizer sgd
echo "FINISHED MLP FOR BATCH SIZE 1024"

python hw1-q2.py mlp -epochs 20 -batch_size 16 -learning_rate 1 -layers 2 -l2_decay 0 -hidden_size 200 -dropout 0.0 -activation relu -optimizer sgd
echo "FINISHED MLP FOR LEARNING RATE 1"
python hw1-q2.py mlp -epochs 20 -batch_size 16 -learning_rate 0.1 -layers 2 -l2_decay 0 -hidden_size 200 -dropout 0.0 -activation relu -optimizer sgd
echo "FINISHED MLP FOR LEARNING RATE 0.1"
python hw1-q2.py mlp -epochs 20 -batch_size 16 -learning_rate 0.01 -layers 2 -l2_decay 0 -hidden_size 200 -dropout 0.0 -activation relu -optimizer sgd

python hw1-q2.py mlp -epochs 150 -batch_size 256 -learning_rate 0.1 -layers 2 -l2_decay 0 -hidden_size 200 -dropout 0.0 -activation relu -optimizer sgd
echo "FINISHED THE OVERFITTING STUDY - NO REG, NO DROPOUT"
python hw1-q2.py mlp -epochs 150 -batch_size 256 -learning_rate 0.1 -layers 2 -l2_decay 0.0001 -hidden_size 200 -dropout 0.0 -activation relu -optimizer sgd
echo "FINISHED THE OVERFITTING STUDY - L2 -> 0.0001, NO DROPOUT"
python hw1-q2.py mlp -epochs 150 -batch_size 256 -learning_rate 0.1 -layers 2 -l2_decay 0 -hidden_size 200 -dropout 0.2 -activation relu -optimizer sgd