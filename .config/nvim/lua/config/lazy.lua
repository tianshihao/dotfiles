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
      "nvim-tree/nvim-web-devicons",
      lazy = true,
    },
    {
      "echasnovski/mini.icons",
      lazy = true,
    },
    {
      "folke/which-key.nvim",
      config = function()
        local wk = require("which-key")
        wk.setup {}
        wk.add({
          { "<leader>t", group = "Telekasten" },
          { "<leader>tf", '<cmd>lua require("telekasten").search_notes()<CR>', desc = "Search in notes" },
          { "<leader>tp", '<cmd>lua require("telekasten").panel()<CR>', desc = "Panel/Palette" },
          { "<leader>tt", '<cmd>lua require("telekasten").goto_today()<CR>', desc = "Goto today" },
          { "<leader>tn", '<cmd>lua require("telekasten").find_daily_notes()<CR>', desc = "Find daily notes" },
          { "<leader>tg", '<cmd>lua require("telekasten").show_tags()<CR>', desc = "Show tags panel" },
        })
      end,
    },
    {
      "oxfist/night-owl.nvim",
      lazy = false,
      priority = 1000,
      config = function()
        require("night-owl").setup()
        vim.api.nvim_create_autocmd("ColorScheme", {
          group = vim.api.nvim_create_augroup("NightOwlMarkdownHeadings", { clear = true }),
          pattern = "night-owl",
          callback = function()
            local backgrounds = { "#24435c", "#382f50", "#203e36", "#413822", "#432e30", "#153842" }
            local foregrounds = { "Title", "Keyword", "DiagnosticOk", "DiagnosticWarn", "Number", "DiagnosticInfo" }
            for level, background in ipairs(backgrounds) do
              vim.api.nvim_set_hl(0, "RenderMarkdownH" .. level, { link = foregrounds[level] })
              local style = { bg = background }
              if level == 1 then
                style.underline = true
                style.overline = true
                style.sp = "#6589a3"
              end
              vim.api.nvim_set_hl(0, "RenderMarkdownH" .. level .. "Bg", style)
            end
          end,
        })
        vim.cmd.colorscheme("night-owl")
      end,
    },
    {
      "nvim-telescope/telescope.nvim",
      dependencies = { "nvim-lua/plenary.nvim" },
      config = function()
        require("telescope").setup {}
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
      "keaising/im-select.nvim",
      config = function()
          require('im_select').setup({
            default_im_select       = "com.apple.keylayout.ABC",
            default_command         = "im-select",
            set_default_events      = { "InsertLeave", "FocusGained" },
            set_previous_events     = { "InsertEnter" },
            keep_quiet_on_no_binary = false,
            async_switch_im         = true,
            async_switch_im_wait    = 100, -- 增加延迟，单位毫秒
          })
      end,
    },
    {
      "MeanderingProgrammer/render-markdown.nvim",
      ft = { "markdown", "telekasten" },
      dependencies = { "nvim-tree/nvim-web-devicons" },
      init = function()
        vim.treesitter.language.register("markdown", "telekasten")
      end,
      opts = {
        render_modes = { "n", "c", "t", "i" },
        anti_conceal = { ignore = { head_background = true } },
        heading = {
          icons = { "▌ ", "▌▌ ", "▌▌▌ ", "▌▌▌▌ ", "▌▌▌▌▌ ", "▌▌▌▌▌▌ " },
          position = "inline",
          sign = false,
          width = "full",
          left_pad = { 0, 2, 4, 6, 8, 10 },
        },
        custom_handlers = { markdown = require("config.markdown_heading_details") },
      },
    },
  },
  install = { colorscheme = { "night-owl" } },
  checker = { enabled = false },
})
