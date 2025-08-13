" ==============================================================================
" My preferred settings.
" ==============================================================================
set secure
set number
set relativenumber
set cursorline
set tabstop=2
set shiftwidth=2
set softtabstop=2
set termencoding=utf-8
set fileencodings=utf-8
set nocompatible
set incsearch
set hlsearch

" ==============================================================================
" Set gvim editor columns.
" ==============================================================================
" set columns=84

" ==============================================================================
" Set font
" ==============================================================================
set guifont=fira_code:h14,sarasa_term_sc:h14

" ==============================================================================
" Set <LEADER>.
" ==============================================================================
let mapleader=" "

" ==============================================================================
" Back to normal mode.
" ==============================================================================
inoremap jj <ESC>

" ==============================================================================
" Save and quit.
" ==============================================================================
nnoremap s :w<CR>
nnoremap x :q<CR>
nnoremap X :q!<CR>

" ==============================================================================
" Swap x/X and t/T, I don't need till.
" ==============================================================================
nnoremap t x
nnoremap T X

" ==============================================================================
" Eliminate highlight caused by /, *, ?.
" ==============================================================================
noremap <C-n> :nohl<CR>

" ==============================================================================
" Accelarate typing.
" ==============================================================================
" inoremap <C-e> `
" inoremap <C-m> =
" inoremap <C-j> <Enter>
" inoremap <C-k> <Esc>O

" ==============================================================================
" Vimilize.
" ==============================================================================
" inoremap gcc :vsc EditAddComments

" ==============================================================================
" Navigating.
" ==============================================================================
nnoremap J :tabn<CR>
nnoremap K :tabp<CR>

" ==============================================================================
" Open the .vimrc anytime I want.
" ==============================================================================
noremap <LEADER>rc :tabnew ~/.vimrc<CR>

function! ToggleBoolean()
    let word = expand("<cword>")
    if word ==# "true"
        silent! execute "normal ciwfalse"
    elseif word ==# "false"
        silent! execute "normal ciwtrue"
    elseif word ==# "True"
        silent! execute "normal ciwFalse"
    elseif word ==# "False"
        silent! execute "normal ciwTrue"
    elseif word ==# "TRUE"
        silent! execute "normal ciwFALSE"
    elseif word ==# "FALSE"
        silent! execute "normal ciwTRUE"
    endif
endfunction

nnoremap <LEADER>tb :call ToggleBoolean()<CR>

runtim! ftplugin/man.vim

set clipboard=unnamedplus

nnoremap <C-r> "
xnoremap <C-r> "
vnoremap <C-r> "
