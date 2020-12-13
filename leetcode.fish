

function leetcode
    set dest (leetcode-cli.py $argv)
    if test $status = 0
      cd $dest
    else
      echo $dest
    end
end
