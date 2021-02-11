import subprocess
import os
import tarfile

class GetMOBSE:
    def __init__(self, name="mobse", env="stand-alone"):

        gitpath = 'https://gitlab.com/mobse/source-code/-/archive/master/source-code-'
        Branches = {
            'stand-alone': 'master',
            'amuse': 'amuse',
            'petar': 'petar'
            }
        if(Branches.get(env)):
            self.branch = env
            self.url = gitpath+Branches.get(env)+'.tar.gz'
            self.tarname = 'source-code-'+Branches.get(env)

        else:
            print("WRONG branch!")
            print("Please choose one from: stand-alone, amuse, petar")
            exit()
        self.version = "1.0" #It will be active in the next future
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
            while os.path.exists(self.name+'.{0}'.format(counter)):
                counter += 1
                if counter > 2: 
                    print(" -----> Be carefull! Too many copy of the folder.")
            os.rename(self.name, self.name+'.{0}'.format(counter))
        os.rename(self.tarname, self.name)
        
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

        tar = tarfile.open(self.tarname+'.tar.gz', 'r:gz')
        tar.extractall()
        tar.close()

        print("---> Rename folder")

        self.rename_dir()

        print("---> done")
        print("-----------------------------------------------------------------------------------")

if __name__ == "__main__":

    instance = GetMOBSE('mobse')
    instance.main()
