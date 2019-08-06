mkdir -p $HOME/.config/leetcode-cli
curl 'https://leetcode.com/api/problems/all/'>"$HOME/.config/leetcode-cli/problem.json"
installed=$(grep LEETCODE $HOME/.profile)
echo $installed
if [[ -z $installed ]];then
    cat leetcode.env>>$HOME/.profile
    cat leetcode.bashrc>>$HOME/.bashrc
    cat leetcode.fish>>$HOME/.config/fish/config.fish
    echo "Please relogin."
fi
