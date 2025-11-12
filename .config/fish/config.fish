# ~/.config/fish/config.fish

function fish_greeting
   echo Welcome back friend!
   echo The time is (set_color yellow; date +%T; set_color normal) and this machine is called $hostname
end

# shell
abbr --add c clear
abbr --add e exit
abbr --add lla ll -a
abbr --add lz lazygit
abbr --add n. nautilus .
abbr --add r ranger
abbr --add y yazi
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
abbr --add gsu git submodule update --init --recursive

# fish
abbr --add fv fish_vi_key_bindings
abbr --add fd fish_default_key_bindings

# set global env var
set -gx ENV_NAME "<PATH_T0_YOUR_ENV_DIR>"

