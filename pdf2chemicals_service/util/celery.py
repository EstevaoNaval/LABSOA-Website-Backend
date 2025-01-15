from celery import Task

class ChainedTask(Task):
    abstract = True    

    def __call__(self, *args, **kwargs):
        if len(args) == 1 and isinstance(args[0], dict):
            kwargs.update(args[0])
            args = ()
        return super(ChainedTask, self).__call__(*args, **kwargs)