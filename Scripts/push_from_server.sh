comment=${1}
num_args=$#

if [[ "${num_args}" == "0" ]];
then
  comment="Forgot to add msg :-("
fi

git add --all
git commit -m "${comment}"
git push