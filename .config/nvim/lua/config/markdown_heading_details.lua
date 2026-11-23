-- Extra decorations alongside render-markdown's inline heading blocks.
local M = { extends = true }
local heading_query

function M.parse(ctx)
  heading_query = heading_query or vim.treesitter.query.parse("markdown", [[
    (atx_heading . (_) @marker)
    (setext_heading [(setext_h1_underline) (setext_h2_underline)] @marker)
  ]])

  local marks, counters = {}, {}
  for _, marker in heading_query:iter_captures(ctx.root, ctx.buf) do
    local level = tonumber(marker:type():match("_h(%d)_"))
    local heading = marker:parent()
    local row, col = heading:start()
    for i = #counters, level + 1, -1 do counters[i] = nil end
    for i = #counters + 1, level - 1 do counters[i] = 0 end
    counters[level] = (counters[level] or 0) + 1

    local group = "RenderMarkdownH" .. level
    marks[#marks + 1] = {
      start_row = row, start_col = col, conceal = "head_icon",
      opts = {
        virt_text = { { "§ " .. table.concat(counters, "."), { group, group .. "Bg" } } },
        virt_text_pos = "eol_right_align",
        priority = 1000,
      },
    }
  end
  return marks
end

return M
