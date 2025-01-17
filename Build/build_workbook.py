import os
import sys
import shutil

# Paths are from Intermediate
mod_dir = '../../Modules'

def usage():
    print('Usage: python3 build_workbook.py <i>')
    print('   or  python3 build_workbook.py all')
    sys.exit(1)

def path_for_chapter_locale_list(mod, chapter, locale_list):
    # Assumes mod has already been stripped of whitespace
    # FIXME: When we start localizing, this will need to be smarter
    return os.path.join(mod_dir, mod, '{}-en_US.tex'.format(chapter))

def build_book(book_id, locale_list, paper_size, draft):
    output_tex_path = 'workbook-{}-{}.tex'.format(book_id, locale_list[0])
    output_pdf_path = 'workbook-{}-{}.pdf'.format(book_id, locale_list[0])
    final_pdf_path = '../{}'.format(output_pdf_path)
    if os.path.exists(final_pdf_path):
        os.remove(final_pdf_path)
    output_tex = open(output_tex_path, 'w')

    # Write the header
    header_file = open('../Support/bookheader.tex', 'r')
    header = header_file.read()
    header_file.close()
    output_tex.write(header)
    
    # Which modules go into the book?
    modlist_filename = 'modlist_{}.txt'.format(book)
    modlist_path = os.path.join(mod_dir, modlist_filename)
    modlist = open(modlist_path, 'r')
    mods = modlist.readlines()
    modlist.close()
    
    for mod in mods:
        trimmed_mod = mod.strip()
        if len(trimmed_mod) > 3:
            # Look for the graphics in the module directory
            gpath_string = '\\graphicspath{{{{../../Modules/{}/}}}}\n'.format(trimmed_mod)
            output_tex.write(gpath_string)
            
            # Which chapters go into the module?
            chapterlist_path = os.path.join(mod_dir, trimmed_mod, 'chapterlist.txt')
            chapterlist = open(chapterlist_path)
            chapters = chapterlist.readlines()
            chapterlist.close()
            for chapter in chapters:
                trimmed_chapter = chapter.strip()
                if len(trimmed_chapter) > 1:
                    chapter_path = path_for_chapter_locale_list(trimmed_mod, trimmed_chapter, locale_list)
                    include_string = '\\input{{{}}}\n'.format(chapter_path)
                    output_tex.write(include_string)

    # Write the footer
    footer_file = open('../Support/bookfooter.tex', 'r')
    footer = footer_file.read()
    footer_file.close()
    output_tex.write(footer)
    output_tex.close()
    os.system('c:\texlive\2022\bin\win32\lualatex {}'.format(output_tex_path))

    if not draft:
        # If a pdf was made, run it again to get cross-references right
        if not draft and os.path.exists(output_pdf_path):
            os.system('c:\texlive\2022\bin\win32\lualatex {}'.format(output_tex_path))
            shutil.move(output_pdf_path, final_pdf_path)
        else:
            print('Build failed')
                
if not os.path.exists('Intermediate'):
    os.mkdir('Intermediate')

if not os.path.exists('user.cfg'):
    shutil.copyfile('Support/default.cfg', 'user.cfg')

if len(sys.argv) < 2:
    usage()
    
arg1 = sys.argv[1]
if arg1 == 'all':
    print ('all not implemented yet')
    sys.exit(1)

book_num = int(arg1)
if book_num == 0:
    usage()

book = str(book_num).zfill(2)
print ('Building workbook ', book)

os.chdir('Intermediate')

build_book(book, ['en_US', 'it_IT'], 'Letter', False)
                        
