from libopensesame.experiment import Experiment
from libopensesame.osexpfile import OSExpReader
from libopensesame.file_pool_store import FilePoolStore
from libopensesame.oslogging import oslogger

cache = {}


class CachedExperiment(Experiment):
    """Allows experiment script and pool folder to be cached to avoid 
    extracting and instantiating multiple times.
    """
    def open(self, src):
        if src in cache:
            oslogger.info(f're-using experiment files and folders: {src}')
            script, self.experiment_path, pool_folder = cache[src]
            self.pool = FilePoolStore(self, folder=pool_folder)
        else:
            oslogger.info(f'creating experiment files and folders: {src}')
            f = OSExpReader(self, src)
            script = f.script
            self.experiment_path = f.experiment_path
            cache[src] = script, self.experiment_path, self.pool.folder()
        return script
