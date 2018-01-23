" Basics
set number
set autoindent
set backspace=indent,eol,start
set complete-=i

" Tabs
set smarttab
set tabstop=2
set shiftwidth=2
set expandtab

" Remove backups and swaps files
set backupcopy=yes
set nobackup
set noswapfile

" Persistent undo
set undofile
set undodir=~/.config/nvim/undo
set undolevels=1000
set undoreload=10000

" Show trailing space
set list
set listchars=tab:\ \ ,trail:·,nbsp:_

call plug#begin('~/.config/nvim/plugged')

" Completion
Plug 'Shougo/deoplete.nvim', { 'do': ':UpdateRemotePlugins' }
Plug 'zchee/deoplete-go', { 'do': 'make'}
Plug 'w0rp/ale'

" Navigation
Plug 'scrooloose/nerdtree'
Plug 'ctrlpvim/ctrlp.vim'
Plug 'vim-airline/vim-airline'
Plug 'vim-airline/vim-airline-themes'

" Languages
Plug 'fatih/vim-go'
Plug 'mxw/vim-jsx'
Plug 'othree/html5.vim'
Plug 'hail2u/vim-css3-syntax'
Plug 'pangloss/vim-javascript'
Plug 'rust-lang/rust.vim'
Plug 'rhysd/vim-crystal'

" Languages utils
Plug 'raimondi/delimitmate'
Plug 'scrooloose/nerdcommenter'

" Themes
Plug 'chriskempson/base16-vim'

call plug#end()

" Colorscheme
let base16colorspace=256
colorscheme base16-tomorrow-night

" Leader
let mapleader=","

" Plugin configs
let g:jsx_ext_required = 0
let g:deoplete#enable_at_startup = 1
let g:ctrlp_custom_ignore = '\v[\/](node_modules|target|dist)|(\.(swp|ico|git|svn))$'

let g:airline_powerline_fonts = 1
let g:airline#extensions#tabline#enabled = 1
let g:airline#extensions#tabline#left_sep = ' '
let g:airline#extensions#tabline#left_alt_sep = ' '
let g:airline#extensions#ale#enabled = 1

let g:go_highlight_functions = 1
let g:go_highlight_methods = 1
let g:go_highlight_fields = 1
let g:go_highlight_types = 1
let g:go_highlight_operators = 1
let g:go_highlight_build_constraints = 1
let g:go_fmt_command = "goimports"

" Mappings
map <C-n> :NERDTreeToggle<CR>
set completeopt-=preview

syntax on
filetype plugin indent on

inoremap <expr><Tab> pumvisible() ? "\<C-n>" : "\<Tab>"
inoremap <expr><S-Tab> pumvisible() ? "\<C-p>" : "\<Tab>"

