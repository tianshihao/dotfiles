-- ============================================================================
-- My preferred settings (converted from .vimrc)
-- ============================================================================
vim.opt.secure = true
vim.opt.number = true
vim.opt.relativenumber = true
vim.opt.cursorline = true
vim.opt.tabstop = 2
vim.opt.shiftwidth = 2
vim.opt.softtabstop = 2
vim.opt.termencoding = "utf-8"
vim.opt.fileencodings = { "utf-8" }
vim.opt.compatible = false
vim.opt.incsearch = true
vim.opt.hlsearch = true

-- Set font (only works in GUI clients)
vim.opt.guifont = "sarasa_term_sc_nerd:h14"

-- Set <LEADER>
vim.g.mapleader = " "

-- Back to normal mode
vim.keymap.set('i', '<C-c>', '<ESC>')

-- Save and quit
vim.keymap.set('n', 's', ':w<CR>')
vim.keymap.set('n', 'x', ':q<CR>')
vim.keymap.set('n', 'X', ':q!<CR>')

-- Swap x/X and t/T
vim.keymap.set('n', 't', 'x')
vim.keymap.set('n', 'T', 'X')

-- Eliminate highlight
vim.keymap.set({'n', 'v'}, '<C-n>', ':nohl<CR>')

-- Accelarate typing
vim.keymap.set('i', '<C-e>', '`')
-- <C-r> in insert mode is not mapped (not working in .vimrc)
vim.keymap.set('i', '<C-j>', '<CR>')
vim.keymap.set('i', '<C-k>', '<Esc>O')

-- Navigating
vim.keymap.set('n', 'J', ':tabn<CR>')
vim.keymap.set('n', 'K', ':tabp<CR>')

-- Open the .vimrc anytime
vim.keymap.set('n', '<leader>rc', ':tabnew ~/.vimrc<CR>')

-- ToggleBoolean function (ported from Vimscript)
local function ToggleBoolean()
  local word = vim.fn.expand('<cword>')
  local replace = {
    ["true"] = "false", ["false"] = "true",
    ["True"] = "False", ["False"] = "True",
    ["TRUE"] = "FALSE", ["FALSE"] = "TRUE",
  }
  if replace[word] then
    vim.cmd('normal! ciw' .. replace[word])
  end
end
vim.keymap.set('n', '<leader>tb', ToggleBoolean)

-- Clipboard
vim.opt.clipboard = "unnamedplus"

-- Source man.vim if available (not directly portable, but can be handled by plugin)
-- vim.cmd('runtime! ftplugin/man.vim')

-- Additional plugin and Lua config can be added below
