local lazypath = vim.fn.stdpath("data") .. "/lazy/lazy.nvim"
if not (vim.uv or vim.loop).fs_stat(lazypath) then
  local lazyrepo = "https://github.com/folke/lazy.nvim.git"
  local out = vim.fn.system({ "git", "clone", "--filter=blob:none", "--branch=stable", lazyrepo, lazypath })
  if vim.v.shell_error ~= 0 then
    error("Failed to clone lazy.nvim: " .. out)
  end
end
vim.opt.rtp:prepend(lazypath)

require("lazy").setup({
  spec = {
    {
      "folke/which-key.nvim",
      config = function()
        local wk = require("which-key")
        wk.setup{}
        wk.register({
          t = {
            name = "+Telekasten",
            f = { '<cmd>lua require("telekasten").search_notes()<CR>', "Search in notes" },
            p = { '<cmd>lua require("telekasten").panel()<CR>', "Panel/Palette" },
            t = { '<cmd>lua require("telekasten").goto_today()<CR>', "Goto today" },
            n = { '<cmd>lua require("telekasten").find_daily_notes()<CR>', "Find daily notes" },
            g = { '<cmd>lua require("telekasten").show_tags()<CR>', "Show tags panel" },
          },
        }, { prefix = '<leader>' })
      end,
    },
    {
      "oxfist/night-owl.nvim",
      lazy = false,
      priority = 1000,
      config = function()
        require("night-owl").setup()
        vim.cmd.colorscheme("night-owl")
      end,
    },
    {
      "nvim-telescope/telescope.nvim",
      dependencies = { "nvim-lua/plenary.nvim" },
      config = function()
        require("telescope").setup{}
      end,
    },
    {
      "renerocksai/telekasten.nvim",
      dependencies = { "nvim-telescope/telescope.nvim" },
      config = function()
        require('telekasten').setup({
          home = vim.fn.expand("~/vault"),
        })
      end,
    },
		{
				"toppair/peek.nvim",
				event = { "VeryLazy" },
				config = function()
						require("peek").setup()
						vim.api.nvim_create_user_command("PeekOpen", require("peek").open, {})
						vim.api.nvim_create_user_command("PeekClose", require("peek").close, {})
				end,
		},
    {
      'nvim-treesitter/nvim-treesitter',
      lazy = false,
      build = ':TSUpdate',
      config = function()
        require("nvim-treesitter").setup({
          ensure_installed = { "markdown", "markdown_inline", "lua", "vim", "vimdoc" },
          auto_install = true,
        })
      end,
    },
    {
      'MeanderingProgrammer/render-markdown.nvim',
      dependencies = { 'nvim-treesitter/nvim-treesitter', 'nvim-mini/mini.nvim' },
      ft = { "markdown", "telekasten" },   -- telekasten 笔记也是 markdown，必须一起加载
      config = function()
        -- 先 setup mini.icons，render-markdown 才能拿到图标
        require("mini.icons").setup()
        -- 让 treesitter 把 telekasten 文件当 markdown 解析，render 才有 parser 可用
        vim.treesitter.language.register("markdown", "telekasten")
        require("render-markdown").setup({
          heading = { enabled = true },
          code = { enabled = true },
          checkbox = { enabled = true },
          table = { enabled = true },
        })
      end,
    },
		{
				"keaising/im-select.nvim",
				config = function()
						local is_windows = vim.fn.has("win32") == 1
						local is_mac     = vim.fn.has("macunix") == 1

						local opts = {
								set_default_events = { "InsertLeave", "CmdlineLeave" },
								set_previous_events = { "InsertEnter" },
								keep_quiet_on_no_binary = false,
								async_switch_im = true,
						}

						if is_windows then
								-- Windows 英文键盘 = 1033
								opts.default_im_select = "1033"
								-- 只在此平台指向 im-select.exe 完整路径（不必加入 PATH）
								opts.default_command = "C:\\Users\\shihao.tian\\im-select.exe"
						elseif is_mac then
								-- macOS 用默认 macism，无需 default_command
								opts.default_im_select = "com.apple.keylayout.ABC"
						else
								-- Linux 用默认 fcitx5-remote / fcitx-remote / ibus
								opts.default_im_select = "xkb:us::eng" -- ibus
						end

						require("im_select").setup(opts)
				end,
		}

  },
  install = { colorscheme = { "night-owl" } },
  checker = { enabled = false },
})
