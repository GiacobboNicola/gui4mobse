import subprocess
import os
import tarfile

class GetMOBSE:
    
    def __init__(self, name="mobse"):
        self.version = "v1.0" #It will be active in the next future
        self.sourcename =  'source-code-'+self.version
        self.tarname = self.sourcename+'.tar'
        self.url = 'https://gitlab.com/mobse/source-code/-/archive/v1.0/'+self.tarname
        self.name = name

    def directory(self):
        maindir = os.path.abspath(os.path.dirname(__file__))
        subdir = os.path.join(maindir, self.name)
        return subdir
    
    def tar_mobse_from_gitlab(self):
        subprocess.run(["curl","-L","-O",self.url])
        #subprocess.run(["wget",self.url])

    def rename_dir(self):
        if os.path.exists(self.name):
            counter = 0
            while os.path.exists(self.name+'_n{0}'.format(counter)):
                counter += 1
                if counter > 2: 
                    print("    |----> Be carefull! Too many copy of the folder.")
            os.rename(self.name, self.name+'_n{0}'.format(counter))
        os.rename(self.sourcename, self.name)
        
    def main(self):
        print("-----------------------------------------------------------------------------------")
        print("downloading version", self.version) 
        print("from", self.url) 
        print("to", self.directory())
        print("-----------------------------------------------------------------------------------")

        self.tar_mobse_from_gitlab()

        print("download completed")
        print("-----------------------------------------------------------------------------------")
        print("---> Untar files")

        tar = tarfile.open(self.tarname)
        tar.extractall()
        tar.close()

        print("---> Rename folder")

        self.rename_dir()

        print("---> done")
        print("-----------------------------------------------------------------------------------")

if __name__ == "__main__":

    instance = GetMOBSE('mobse')
    instance.main()
