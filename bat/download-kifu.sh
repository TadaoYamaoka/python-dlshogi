# This shell script is supposed to run in a Datalab container to
# download Shogi kifu from Floodgate.
set -x
mkdir -p ../kifu/zip 
cd ../kifu/zip
time wget -c --trust-server-names "https://osdn.net/frs/redir.php?m=jaist&f=shogi-server%2F68500%2Fwdoor2016.7z"
cd ..
which 7z || apt-get update -y && apt-get install -y p7zip-full --allow-unauthenticated
[ -d 2016 ] || time 7z x zip/wdoor2016.7z -aos # -y

cd ../python-dlshogi
pip install python-shogi statistics tqdm
pip install --no-cache-dir -e .
time python utils/filter_csa.py ../kifu/2016/ # 20 minutes
time python utils/make_kifu_list.py ../kifu/2016/ ../kifu/kifulist
time python pydlshogi/read_kifu.py ../kifu/kifulist_test.txt
time python pydlshogi/read_kifu.py ../kifu/kifulist_train.txt
