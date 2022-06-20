comment=${1}
num_args=$#

if [[ "${num_args}" == "0" ]];
then
  comment="Forgot to add msg :-("
fi

cd /Users/kaspara/Documents/MASTER_GIT_GAMMEL_MAC/MasterThesis
git pull
zsh copy_files.sh
cd /Users/kaspara/Documents/MASTER_GIT_GAMMEL_MAC/daniel_repo
git pull
git add --all
git commit -m "${comment}"
git push
