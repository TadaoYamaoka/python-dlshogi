# This Shell script downloads Shogi kifu from Floodgate and create pickle files
set -x
mkdir -p ../kifu/zip 
cd ../kifu/zip
time wget -c --trust-server-names "https://osdn.net/frs/redir.php?m=jaist&f=shogi-server%2F68500%2Fwdoor2016.7z"
cd ..
time 7z x zip/wdoor2016.7z -aos # -y

cd ../python-dlshogi
pip install python-shogi tqdm
pip install --no-cache-dir -e .
time python utils/filter_csa.py ../kifu/2016/ # 20 minutes
time python utils/make_kifu_list.py ../kifu/2016/ ../kifu/kifulist
time python pydlshogi/read_kifu.py ../kifu/kifulist_test.txt
time python pydlshogi/read_kifu.py ../kifu/kifulist_train.txt
