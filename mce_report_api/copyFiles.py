import shutil
import os
def copyPhotos(surveyID):
    # Copy directory tree (cp -R src dst) form remote location "shared folder"
    src='../'+surveyID
    #srcDir = os.path.dirname(src)

    # The destination directory on the machine that run this script
    # It will be copied by the same name.
    dst='./output/'+surveyID+'/'


    if os.path.exists(src):
        if not os.path.exists(dst):
            shutil.copytree(src, dst)
        else:
            print( 'Warrning: Photos Directory already exist')
    else:
        print( 'Error: Photos Directory Does''t exist')
    return dst

if __name__=='__main__':
    copyPhotos('104747')
