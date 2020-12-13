# export LEETCODE_PATH=$HOME/code/leetcode/
leetcode() {
    dest=`leetcode-cli.py $*`
    if test $? -eq 0; then  
        cd $dest
    else 
        echo $dest
    fi
}
