Set-Alias lz lazygit
function e { exit }
function src {
    if ($args.Count -eq 0) {
        . $PROFILE
    } else {
        . $args[0]
    }
}
function s { src }
function ls { Get-ChildItem -Force -al }
function mv { Move-Item }
Remove-Item alias:rm -ErrorAction SilentlyContinue
function rm {
    param([Parameter(ValueFromRemainingArguments=$true)][string[]]$Args)
    $force = $Args -contains '-f' -or $Args -contains '-rf'
    $recurse = $Args -contains '-r' -or $Args -contains '-rf'
    $paths = $Args | Where-Object { $_ -notmatch '^-.*' }
    foreach ($path in $paths) {
        Remove-Item $path -Force:($force) -Recurse:($recurse)
    }
}

function gaa { git add . }
function gb { git branch }
function gba { git branch -a }
function gbd { git branch -D @args }
function gbdr { git branch -D -r @args }
function gca { git commit --amend @args }
function gcf { git clean -f @args }
function gcm { git commit -m @args }
function gcn { git clean -n @args }
function gco { git checkout @args }
function gcod { git checkout . }
function gcob { git checkout -b @args }
function gcom { git checkout master }
function gcp { git cherry-pick @args }
function gcpa { git cherry-pick --abort }
function gcpc { git cherry-pick --continue }
function gcz { git cz @args }
function gl { git log @args }
function glo { git log --oneline @args }
function gpl { git pull @args }
function gplr { git pull -r @args }
function gpof { git push origin --force @args }
function gps { git push @args }
function grb { git rebase @args }
function grba { git rebase --abort }
function grbc { git rebase --continue }
function grbi { git rebase -i @args }
function grbm { git rebase master }
function grbs { git rebase --skip }
function grh { git reset --hard @args }
function grhh { git reset --hard HEAD }
function grhh1 { git reset --hard HEAD^ }
function grhh10 { git reset --hard HEAD^^^^^^^^^ }
function grs { git reset --soft @args }
function grsh { git reset --soft HEAD }
function grsh1 { git reset --soft HEAD^ }
function gs { git status @args }
function gst { git stash @args }
function gsta { git stash apply @args }
function gstl { git stash list }
function gstp { git stash pop }
function gsts { git stash save @args }