# ~/.config/fish/config.fish

function fish_greeting
   echo Welcome back friend!
   echo The time is (set_color yellow; date +%T; set_color normal) and this machine is called $hostname
end

# shell
abbr --add c clear
abbr --add e exit
abbr --add lz lazygit
abbr --add r ranger
abbr --add lla ll -a
abbr --add s source ~/.config/fish/config.fish

# git
abbr --add gaa git add .
abbr --add gb git branch
abbr --add gba git branch -a
abbr --add gbd git branch -D
abbr --add gbdr git branch -D -r
abbr --add gca git commit --amend
abbr --add gcf git clean -f
abbr --add gcm git commit -m
abbr --add gcn git clean -n
abbr --add gco git checkout
abbr --add gco. git checkout .
abbr --add gcob git checkout -b
abbr --add gcom git checkout master
abbr --add gcp git cherry-pick
abbr --add gcpa git cherry-pick --abort
abbr --add gcpc git cherry-pick --continue
abbr --add gcz git cz
abbr --add gl git log
abbr --add glo git log --oneline
abbr --add gpl git pull
abbr --add gplr git pull -r
abbr --add gpof git push origin --force
abbr --add gps git push
abbr --add grb git rebase
abbr --add grba git rebase --abort
abbr --add grbc git rebase --continue
abbr --add grbi git rebase -i
abbr --add grbm git rebase master
abbr --add grbs git rebase --skip
abbr --add grh git reset --hard
abbr --add grhh git reset --hard HEAD
abbr --add grhh1 git reset --hard HEAD^
abbr --add grhh10 git reset --hard HEAD^^^^^^^^^
abbr --add grs git reset --soft
abbr --add grsh git reset --soft HEAD
abbr --add grsh1 git reset --soft HEAD^
abbr --add gs git status
abbr --add gst git stash
abbr --add gsta git stash apply
abbr --add gstl git stash list
abbr --add gstp git stash pop
abbr --add gsts git stash save 

# nautilos
abbr --add n. nautilus .

# yazi
abbr --add y yazi

function rename-branch
    set -l old_branch (git symbolic-ref --short HEAD)
    set -l new_branch $argv[1]
    if test -n "$new_branch"
        git branch -m $old_branch $new_branch
        echo "Branch renamed from $old_branch to $new_branch"
    else
        echo "Please provide a new branch name"
    end
end

function rebase-current-branch-to
    set -l current_branch (git symbolic-ref --short HEAD)
    set -l target_branch $argv[1]
    if test -n "$target_branch"
        git rebase $target_branch $current_branch
        echo "Rebased $current_branch onto $target_branch"
    else
        echo "Please provide a target branch name"
    end
end
abbr --add rcbt rebase-current-branch-to

# Check if the platform is macOS
if string match -q "Darwin" (uname)
    # Add directories to PATH for macOS
    set -gx PATH /usr/local/bin /System/Cryptexes/App/usr/bin /usr/bin /bin /usr/sbin /opt/homebrew/bin $PATH
else if string match -q "Linux" (uname)
    set -gx PATH /usr/local/cuda-11.6/bin/ $PATH
    # Add directories to PATH for other platforms
end

function checkout-branch
    if not set -q argv[1]
        echo "Please provide a branch name."
        return 1
    end

    git checkout -b $argv[1]
end

# 自动补全功能
function __fish_complete_branches
    set current_branch (git rev-parse --abbrev-ref HEAD 2> /dev/null)
    set branches (git for-each-ref --format='%(refname:short)' refs/heads/ | grep -v HEAD)

    # 输出当前分支名，然后是其他分支
    if set -q current_branch
        echo $current_branch
        for branch in $branches
            if test $branch != $current_branch
                echo $branch
            end
        end
    else
        echo $branches
    end
end

# 为 checkout-branch 函数启用自动补全
complete -c checkout-branch -a "(__fish_complete_branches)" -n "not __fish_seen_subcommand_from checkout-branch"
