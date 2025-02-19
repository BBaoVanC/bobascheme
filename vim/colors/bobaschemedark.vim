set background=dark
highlight clear
syntax reset

let g:colors_name = "bobaschemedark"

let s:fg = "#d4d4d4"
let s:bg = "#111111"

let s:gray = "#414141"

let s:dark_black    = "#2b2b2b"
let s:dark_red      = "#b04744"
let s:dark_yellow   = "#8c6110"
let s:dark_green    = "#167a42"
let s:dark_cyan     = "#29757f"
let s:dark_blue     = "#216dbf"
let s:dark_magenta  = "#9f4b95"
let s:dark_white    = "#bfbfbf"

let s:black         = "#5e5e5e"
let s:red           = "#eb7c74"
let s:yellow        = "#b78738"
let s:green         = "#54b073"
let s:cyan          = "#61aab3"
let s:blue          = "#66a1f8"
let s:magenta       = "#d87fcc"
let s:white         = "#e9e9e9"

let s:link_color    = "#3a94fb"


function! s:hl(group, fg, bg, attr)
  exec "highlight "
  \ . a:group
  \ . (a:fg != "" ? (" guifg=" . a:fg) : "")
  \ . (a:bg != "" ? (" guibg=" . a:bg) : "")
  \ . (a:attr != "" ? (" gui=" . a:attr . " cterm=" . a:attr) : " gui=NONE cterm=NONE")
endfun

" ==> Colors
call s:hl("Normal", s:fg, "", "")
call s:hl("MatchParen", s:fg, s:black, "")
call s:hl("Whitespace", s:black, "", "")
call s:hl("NonText", s:black, "", "")
call s:hl("Title", s:fg, "", "bold")

call s:hl("SpellBad", "", "", "undercurl guisp=" . s:dark_red)
call s:hl("SpellCap", "", "", "undercurl guisp=" . s:dark_green)
call s:hl("SpellLocal", "", "", "undercurl guisp=" . s:dark_yellow)
call s:hl("SpellRare", "", "", "undercurl guisp=" . s:dark_blue)

call s:hl("ColorColumn", "", s:dark_black, "")
call s:hl("Cursor", s:dark_black, s:fg, "")
call s:hl("CursorColumn", "", s:dark_black, "")
call s:hl("CursorLine", "", s:dark_black, "")
call s:hl("LineNr", s:black, "", "")
call s:hl("CursorLineNr", s:fg, s:dark_black, "")

call s:hl("Folded", s:fg, s:dark_black, "")
call s:hl("Visual", "", s:gray, "")
call s:hl("VisualNOS", "", s:gray, "")

call s:hl("Search", s:bg, s:dark_yellow, "")
call s:hl("IncSearch", s:bg, s:yellow, "")

call s:hl("Pmenu", s:fg, s:dark_black, "")
call s:hl("PmenuSel", s:white, s:dark_blue, "")
call s:hl("PmenuSbar", "", s:black, "")
call s:hl("PmenuThumb", "", s:fg, "")

set foldcolumn=auto:9
call s:hl("SignColumn", "", s:bg, "")
call s:hl("FoldColumn", s:dark_blue, s:bg, "")

call s:hl("WinSeparator", s:dark_black, s:bg, "")

call s:hl("WarningMsg", s:fg, s:dark_yellow, "")
call s:hl("ErrorMsg", s:fg, s:dark_red, "")
call s:hl("Question", s:dark_green, "", "bold")

call s:hl("StatusLine", s:fg, s:dark_black, "bold")
call s:hl("StatusLineNC", s:black, s:dark_black, "")
call s:hl("TabLine", s:black, s:dark_black, "")
call s:hl("TabLineSel", s:white, s:black, "bold")
call s:hl("TabLineFill", "", s:dark_black, "")


call s:hl("DiffAdd", s:white, s:dark_green, "")
call s:hl("DiffChange", s:white, s:dark_yellow, "")
call s:hl("DiffDelete", s:white, s:dark_red, "")
call s:hl("DiffText", s:white, s:dark_blue, "")
" GitGutter
call s:hl("GitGutterAdd", s:dark_green, s:bg, "")
call s:hl("GitGutterDelete", s:dark_red, s:bg, "")
call s:hl("GitGutterChange", s:dark_yellow, s:bg, "")
call s:hl("GitGutterChangeDelete", s:dark_red, s:bg, "")
" Fugitive
call s:hl("diffAdded", s:dark_green, "", "")
call s:hl("diffRemoved", s:dark_red, "", "")
" vim-signify
call s:hl("SignifySignAdd", s:dark_green, s:bg, "")
call s:hl("SignifySignDelete", s:dark_red, s:bg, "")
call s:hl("SignifySignChange", s:dark_yellow, s:bg, "")
call s:hl("SignifySignChangeDelete", s:dark_red, s:bg, "")


" Syntax
call s:hl("Comment", s:black, "", "italic")

call s:hl("Constant", s:dark_yellow, "", "")
call s:hl("String", s:dark_green, "", "")
call s:hl("Character", s:dark_green, "", "")

call s:hl("Identifier", s:dark_cyan, "", "")

call s:hl("Statement", s:dark_magenta, "", "")

call s:hl("PreProc", s:dark_red, "", "")
call s:hl("Macro", s:dark_red, "", "bold")
call s:hl("Include", s:dark_blue, "", "")

call s:hl("Type", s:dark_blue, "", "bold")

call s:hl("Special", s:dark_yellow, "", "bold")
call s:hl("SpecialComment", s:dark_magenta, "", "italic")
call s:hl("Delimiter", s:fg, "", "")
call s:hl("Debug", "", "", "inverse")
call s:hl("Tag", "", "", "inverse")

call s:hl("Underlined", s:link_color, "", "underline")
call s:hl("Error", s:dark_red, s:bg, "inverse")
call s:hl("Todo", s:dark_yellow, s:bg, "bold")


" Misc
call s:hl("Directory", s:dark_cyan, "", "")
