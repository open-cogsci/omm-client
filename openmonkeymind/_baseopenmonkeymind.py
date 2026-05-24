"""An instance of `BaseOpenMonkeyMind` lives as the `omm` object in the Python 
workspace in OpenSesame experiments.

In a Python `inline_script`, you can check whether an experiment is being
run in the context of OpenMonkeyMind (as opposed to being launched directly
from within OpenSesame) like so:

```py
# In an initialization script, detect whether `omm` is available.
if 'omm' not in globals() or not omm.connected:
    omm = None

# Elsewhere, make code contingent on whether `omm` is available.
if omm is not None:
    # OpenMonkeyMind functionality
else:
    # Dummy functionality
```
"""

from libopensesame.py3compat import *
from libopensesame.experiment import Experiment

class BaseJob:

    """A job consisting of a state, an id, and job/result variables.

    A job consists of:
    - A state, which can be PENDING, STARTED, or FINISHED.
    - An id, which uniquely identifies the job. The id is not an index, i.e.,
      it does not indicate the position of the job in the job table.
    - A set of job variables, such as experimental conditions.
    - A set of result variables, such as response variables. A job can have
      multiple result variables if the job has been reset and then repeated. In
      that case, the last set of result variables is included.

    """

    # Job states
    PENDING = 1
    STARTED = 2
    FINISHED = 3

    def __init__(self):

        self._state = None
        self._id = None
        self._data = {}

    @property
    def state(self) -> int:

        """The state of the job.

        Returns
        -------
        int
            The state of the job (PENDING, STARTED, or FINISHED).
        """

        return self._state

    @property
    def id_(self) -> int:

        """The unique identifier of the job.

        Returns
        -------
        int
            The unique identifier of the job.
        """

        return self._id

    @property
    def finished(self) -> bool:

        """Indicates whether the job is finished.

        Returns
        -------
        bool
            True if the job is finished, False otherwise.
        """

        return self._state == BaseJob.FINISHED

    @property
    def started(self) -> bool:

        """Indicates whether the job has started.

        Returns
        -------
        bool
            True if the job has started, False otherwise.
        """

        return self._state == BaseJob.STARTED

    @property
    def pending(self) -> bool:

        """Indicates whether the job is pending.

        Returns
        -------
        bool
            True if the job is pending, False otherwise.
        """

        return self._state == BaseJob.PENDING

    def __getitem__(self, key):

        return self._data[key]

    def __iter__(self):

        for key, value in self._data.items():
            yield key, value

    def __eq__(self, other):

        return (
            self.id_ == other.id_ and
            self.state == other.state and
            self._data == other._data
        )

    def __str__(self):

        return '{}:{}:{}'.format(self.id_, self.state, self._data)

    def __repr__(self):

        return '{}:{}:{}'.format(self.id_, self.state, self._data)

    def __contains__(self, key):

        return key in self._data

    def __delitem__(self, key):

        del self._data[key]

class BaseOpenMonkeyMind(object):

    """Allows for programmatic interaction with the OpenMonkeyMind server.

    Lives as the `omm` object in the Python workspace in OpenSesame
    experiments.
    """

    def __init__(self):

        self._participant = None
        self._alternate_participant_id = None
        self._participant_name = None
        self._experiment = None
        self._job_id = None
        self._study = None
        self._job_count = None
        self._participant_metadata = {}

    @property
    def current_participant(self) -> str:

        """The identifier of the currently announced participant.

        Returns
        -------
        str
            The identifier of the currently announced participant.
        """

        return self._participant

    @property
    def current_alternate_participant_id(self) -> str:

        """The alternate identifier of the currently announced participant.

        Returns
        -------
        str
            The alternate identifier of the currently announced participant.
        """

        return self._alternate_participant_id

    @property
    def current_participant_ids(self) -> tuple(str, str):

        """A tuple with the participant identifier and the alternate participant identifier.

        Returns
        -------
        tuple
            A tuple containing the participant identifier and the alternate
            participant identifier.
        """
        return self._participant, self._alternate_participant_id

    @property
    def current_participant_changed(self) -> bool:

        """Indicates whether a new participant identifier is available.

        If this is true, the current participant is not automatically changed.
        Rather, this property allows the system to check whether a new
        participant would be identified if we would detect again.

        Returns
        -------
        bool
            True if a new participant identifier is available, False otherwise.
        """
        return False

    @property
    def current_participant_name(self) -> str:

        """The name of the currently announced participant.

        Returns
        -------
        str
            The name of the currently announced participant.
        """

        return self._participant_name

    @property
    def participant_metadata(self) -> dict:

        """A dict with metadata of the participant.

        Returns
        -------
        dict
            A dictionary containing metadata of the participant.
        """

        return self._participant_metadata

    @property
    def current_study(self) -> int:

        """The id of the current study.

        Returns
        -------
        int
            The id of the current study.
        """

        return self._study

    @property
    def current_job(self) -> int:

        """The id of the current job.

        This does not correspond to the position of the job in the job table.
        For that, see `get_current_job_index()`.

        Returns
        -------
        int
            The id of the current job.
        """

        return self._job_id

    @property
    def job_count(self) -> int:

        """The number of jobs in the job table.

        Returns
        -------
        int
            The number of jobs in the job table.
        """

        return self._job_count

    @property
    def connected(self) -> bool:

        """Indicates whether the client is connected to a server.

        Returns
        -------
        bool
            True when connected to a server, False otherwise.
        """

        return self._participant is not None

    @property
    def available(self) -> bool:

        """Indicates whether a server appears to be available.

        Returns
        -------
        bool
            True when a server appears to be available, False otherwise.
        """

        raise NotImplementedError()

    def announce(self, participant: str) -> Experiment:

        """Announces a new participant and retrieves the experiment file for that participant.

        The returned experiment is now the current experiment. The participant is
        now the current participant.

        Parameters
        ----------
        participant : str
            A participant id. This may be the canonical or alternate identifier.

        Returns
        -------
        Experiment
            An experiment object.
        """

        pass

    def request_job(self, job_index: int = None) -> BaseJob:

        """Gets a job for the current experiment and participant.

        Specifically, the first job with a PENDING or STARTED status. The
        returned job is now the current job. The state of the job on the server
        is set to STARTED.

        Parameters
        ----------
        job_index : int, optional
            The index of the job to request. If this is None, then the next open
            job (i.e. the first job with a PENDING or STARTED status) is retrieved.

        Returns
        -------
        BaseJob
            A Job object.
        """

        pass

    def send_current_job_results(self, job_results: dict):

        """Sends results for the current job.

        This changes the current job status to FINISHED. There is now no current
        job anymore.

        Parameters
        ----------
        job_results : dict
            A dictionary where keys are experimental variables, and values are values.
        """

        pass

    def get_current_job_index(self) -> int:

        """Gets the index of the current job in the job table.

        This reflects the order of the job table and is therefore different
        from the job id as provided by the `current_job` property.

        Returns
        -------
        int
            The index of the current job in the job table.
        """

        pass

    def get_jobs(self, from_index: int, to_index: int) -> list[BaseJob]:

        """Gets all jobs between `from_index` and `to_index`.

        `to_index` is not included (i.e. Python-slice style). The first job has
        index 1. This does not change the current job.

        Parameters
        ----------
        from_index : int
            The starting index (inclusive).
        to_index : int
            The ending index (exclusive).

        Returns
        -------
        list[BaseJob]
            A list of Job objects.
        """

        pass

    def insert_jobs(self, index: int, jobs: list[dict]):

        """Inserts a list of jobs at the specified index.

        The first job in the list has the specified index. The first job has
        index 1. There is now no current job anymore.

        Parameters
        ----------
        index : int
            The index at which to insert the jobs.
        jobs : list[dict]
            A list of dictionaries (not Job objects), where the variables and
            values are keys and values of the dict.
        """

        pass

    def delete_jobs(self, from_index: int, to_index: int):

        """Deletes all jobs between `from_index` and `to_index`.

        `to_index` is not included (i.e. Python-slice style). There is now no
        current job anymore.

        Parameters
        ----------
        from_index : int
            The starting index (inclusive).
        to_index : int
            The ending index (exclusive).
        """

        pass

    def set_job_states(self, from_index: int, to_index: int, state: int):

        """Sets the states of all jobs between `from_index` and `to_index`.

        `to_index` is not included (i.e. Python-slice style). The first job has
        index 1. There is now no current job anymore.

        If a job already had results and is set to open, then the results are
        not reset. Rather, the job will get a second set of results.

        Parameters
        ----------
        from_index : int
            The starting index (inclusive).
        to_index : int
            The ending index (exclusive).
        state : int
            The state to set (Job.PENDING, Job.STARTED, or Job.FINISHED).
        """

        pass

    @property
    def generic_study_data(self) -> object:

        """General-purpose data specific to the current study but shared across all participants.

        The data can be any object that can be serialized by JSON. If no data
        has been set, it has the value `None`.

        Returns
        -------
        object
            The general-purpose data specific to the current study.
        """

        pass

    @generic_study_data.setter
    def generic_study_data(self, val: object):

        """Set the general-purpose data specific to the current study.

        Parameters
        ----------
        val : object
            The data to set. Must be serializable by JSON.
        """

        pass

    @property
    def generic_participant_data(self) -> object:

        """General-purpose data specific to the current participant but shared across all studies.

        The data can be any object that can be serialized by JSON. If no data
        has been set, it has the value `None`.

        Returns
        -------
        object
            The general-purpose data specific to the current participant.
        """

        pass

    @generic_participant_data.setter
    def generic_participant_data(self, val: object):

        """Set the general-purpose data specific to the current participant.

        Parameters
        ----------
        val : object
            The data to set. Must be serializable by JSON.
        """

        pass

    @property
    def generic_session_data(self) -> object:

        """General-purpose data specific to the current participant and study.

        The data can be any object that can be serialized by JSON. If no data
        has been set, it has the value `None`.

        Returns
        -------
        object
            The general-purpose data specific to the current participant and study.
        """

        pass

    @generic_session_data.setter
    def generic_session_data(self, val: object):

        """Set the general-purpose data specific to the current participant and study.

        Parameters
        ----------
        val : object
            The data to set. Must be serializable by JSON.
        """

        pass
        pass

    def __reduce__(self):

        """Avoids an error during unpickling.

        Returns
        -------
        tuple
            A tuple to avoid unpickling errors.
        """

        return (object, ())