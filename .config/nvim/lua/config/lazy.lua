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
  },
  install = { colorscheme = { "night-owl" } },
  checker = { enabled = false },
})
