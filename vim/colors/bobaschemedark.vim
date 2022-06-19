set background=dark
highlight clear
syntax reset

let g:colors_name = "bobaschemedark"

let s:fg = "#d4d4d4"
let s:bg = "#111111"

" lightness: 0, 10, 20, 30
let s:black0 = "#000000"
let s:black1 = "#212121"
let s:black2 = "#303030"
let s:text_dark_gray = "#474747"

" lightness: 100, 90, 80, 70
let s:white0 = "#ffffff"
let s:white1 = "#e2e2e2"
let s:white2 = "#c6c6c6"
let s:white3 = "#ababab"

let s:dark_red      = "#b04744"
let s:dark_yellow   = "#7a6904"
let s:dark_green    = "#167a42"
let s:dark_cyan     = "#29757f"
let s:dark_blue     = "#216dbf"
let s:dark_magenta  = "#9f4b95"
let s:dark_white    = "#bfbfbf"

let s:red     = "#eb7c74"
let s:yellow  = "#b19c3f"
let s:green   = "#54b073"
let s:cyan    = "#61aab3"
let s:blue    = "#66a1f8"
let s:magenta = "#d87fcc"


function! s:hl(group, fg, bg, attr)
  exec "highlight "
  \ . a:group
  \ . (a:fg != "" ? (" guifg=" . a:fg) : "")
  \ . (a:bg != "" ? (" guibg=" . a:bg) : "")
  \ . (a:attr != "" ? (" gui=" . a:attr . " cterm=" . a:attr) : " gui=NONE cterm=NONE")
endfun

" ==> Colors
call s:hl("Normal", s:fg, s:bg, "")

call s:hl("Cursor", s:black0, s:fg, "")
call s:hl("CursorColumn", "", s:black1, "")
call s:hl("CursorLine", "", s:black1, "")
call s:hl("LineNr", s:text_dark_gray, "", "")
call s:hl("CursorLineNr", s:fg, "", "")

call s:hl("DiffAdd", "", s:dark_green, "")
call s:hl("DiffChange", "", s:dark_yellow, "")
call s:hl("DiffDelete", "", s:dark_red, "")
call s:hl("DiffText", "", s:dark_blue, "")

call s:hl("Search", s:black0, s:dark_yellow, "")
call s:hl("IncSearch", s:black0, s:yellow, "")
