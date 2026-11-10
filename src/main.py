import sys 

from copy_static import copy_from_source_to_destination

from gencontent import generate_pages_recursive


# !! FOR WEB BUILDING Docs Directory Path
docs_dir_path = "docs"

# Static Directory Path
static_dir_path = "static"
# Content Directory Path
content_dir_path = "content"
# Template HTML file path
template_path = "template.html"

# !! FOR LOCAL TESTING Public Directory Path
dir_path_public = "public"


def main():

    # grabbing basepath  
    if len(sys.argv) > 1:      # the sys.argv to grab the first CLI argument to the program. Save it as the basepath. If one isn't provided, default to /
        basepath = sys.argv[1]
    else:
        basepath = "/"              # defaults to "/" path for local testing and building

    # file content copying
    print(f'deleting public directory: {docs_dir_path}')

    print(f'copying static files to public directory: {static_dir_path} -> {docs_dir_path}')

    copy_from_source_to_destination( static_dir_path, docs_dir_path )

    # page generation
    print("Generating pages...")         
                                # 2. should generate a page for every markdown file in the content directory and write the results to the public directory.
    generate_pages_recursive( 
        content_dir_path, 
        template_path, 
        docs_dir_path,
        basepath
        )    



if __name__ == "__main__":
    main()



# basepath explanation
"""
page generator then needs to use basepath when it rewrites links, replacing href="/ with href="{basepath} and src="/ with src="{basepath}. 
This is what makes the site work at https://USERNAME.github.io/REPO_NAME/ instead of only at the domain root.
"""
