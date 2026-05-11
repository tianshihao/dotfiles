-- ============================================================================
-- Basic Editor Settings
-- ============================================================================
vim.opt.secure = true
vim.opt.number = true
vim.opt.relativenumber = true
vim.opt.cursorline = true
vim.opt.tabstop = 2
vim.opt.shiftwidth = 2
vim.opt.softtabstop = 2
-- vim.opt.termencoding = "utf-8"
vim.opt.fileencodings = { "utf-8" }
vim.opt.compatible = false
vim.opt.incsearch = true
vim.opt.hlsearch = true


-- ============================================================================
-- Font settings (only for GUI clients)
-- ============================================================================
vim.opt.guifont = "Sarasa Term SC Nerd:h20"


-- ============================================================================
-- Neovide specific settings
-- ============================================================================
if vim.g.neovide then
  vim.g.neovide_font_hinting = "none"
  vim.g.neovide_font_edging = "antialias"
end


-- ============================================================================
-- Keymap settings
-- ============================================================================
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
-- Accelerate typing
vim.keymap.set('i', '<C-e>', '`')
-- <C-r> in insert mode is not mapped (not working in .vimrc)
vim.keymap.set('i', '<C-j>', '<CR>')
vim.keymap.set('i', '<C-k>', '<Esc>O')
-- Tab navigation
vim.keymap.set('n', 'J', ':tabn<CR>')
vim.keymap.set('n', 'K', ':tabp<CR>')


-- ============================================================================
-- Plugin-related keymaps

-- Telekasten 快捷键已在 which-key 的 lazy.lua 配置中注册


-- ============================================================================
-- Platform detection and path variables
-- ============================================================================
local is_windows = vim.fn.has('win32') == 1 or vim.fn.has('win64') == 1


-- ============================================================================
-- Config file paths and related keymaps
-- ============================================================================
local config_dir, init_path, lazy_path
if is_windows then
  -- Windows: ~/AppData/Local/nvim/
  config_dir = vim.fn.expand('~/AppData/Local/nvim')
  init_path = config_dir .. '/init.lua'
  lazy_path = config_dir .. '/lua/config/lazy.lua'
else
  -- Linux/Mac: ~/.config/nvim/
  config_dir = vim.fn.expand('~/.config/nvim')
  init_path = config_dir .. '/init.lua'
  lazy_path = config_dir .. '/lua/config/lazy.lua'
end

-- Open init.lua
vim.keymap.set('n', '<leader>rc', ':tabnew ' .. init_path .. '<CR>')

-- Open lazy.lua
vim.keymap.set('n', '<leader>lz', ':tabnew ' .. lazy_path .. '<CR>')

-- Reload init.lua config
vim.keymap.set('n', '<leader>r', ':source ' .. init_path .. '<CR>')


-- ============================================================================
-- Clipboard settings
-- ============================================================================
if vim.fn.has('clipboard') == 1 then
  if is_windows then
    vim.opt.clipboard = 'unnamed'
  else
    vim.opt.clipboard = 'unnamedplus'
  end
end


-- ============================================================================
-- Load lazy.nvim plugin manager
-- ============================================================================
require("config.lazy")

