# Table of Contents

* [openmonkeymind.\_baseopenmonkeymind](#openmonkeymind._baseopenmonkeymind)
  * [BaseJob](#openmonkeymind._baseopenmonkeymind.BaseJob)
    * [state](#openmonkeymind._baseopenmonkeymind.BaseJob.state)
    * [id\_](#openmonkeymind._baseopenmonkeymind.BaseJob.id_)
    * [finished](#openmonkeymind._baseopenmonkeymind.BaseJob.finished)
    * [started](#openmonkeymind._baseopenmonkeymind.BaseJob.started)
    * [pending](#openmonkeymind._baseopenmonkeymind.BaseJob.pending)
  * [BaseOpenMonkeyMind](#openmonkeymind._baseopenmonkeymind.BaseOpenMonkeyMind)
    * [current\_participant](#openmonkeymind._baseopenmonkeymind.BaseOpenMonkeyMind.current_participant)
    * [current\_alternate\_participant\_id](#openmonkeymind._baseopenmonkeymind.BaseOpenMonkeyMind.current_alternate_participant_id)
    * [current\_participant\_ids](#openmonkeymind._baseopenmonkeymind.BaseOpenMonkeyMind.current_participant_ids)
    * [current\_participant\_changed](#openmonkeymind._baseopenmonkeymind.BaseOpenMonkeyMind.current_participant_changed)
    * [current\_participant\_name](#openmonkeymind._baseopenmonkeymind.BaseOpenMonkeyMind.current_participant_name)
    * [participant\_metadata](#openmonkeymind._baseopenmonkeymind.BaseOpenMonkeyMind.participant_metadata)
    * [current\_study](#openmonkeymind._baseopenmonkeymind.BaseOpenMonkeyMind.current_study)
    * [current\_job](#openmonkeymind._baseopenmonkeymind.BaseOpenMonkeyMind.current_job)
    * [job\_count](#openmonkeymind._baseopenmonkeymind.BaseOpenMonkeyMind.job_count)
    * [connected](#openmonkeymind._baseopenmonkeymind.BaseOpenMonkeyMind.connected)
    * [available](#openmonkeymind._baseopenmonkeymind.BaseOpenMonkeyMind.available)
    * [announce](#openmonkeymind._baseopenmonkeymind.BaseOpenMonkeyMind.announce)
    * [request\_job](#openmonkeymind._baseopenmonkeymind.BaseOpenMonkeyMind.request_job)
    * [send\_current\_job\_results](#openmonkeymind._baseopenmonkeymind.BaseOpenMonkeyMind.send_current_job_results)
    * [get\_current\_job\_index](#openmonkeymind._baseopenmonkeymind.BaseOpenMonkeyMind.get_current_job_index)
    * [get\_jobs](#openmonkeymind._baseopenmonkeymind.BaseOpenMonkeyMind.get_jobs)
    * [insert\_jobs](#openmonkeymind._baseopenmonkeymind.BaseOpenMonkeyMind.insert_jobs)
    * [delete\_jobs](#openmonkeymind._baseopenmonkeymind.BaseOpenMonkeyMind.delete_jobs)
    * [set\_job\_states](#openmonkeymind._baseopenmonkeymind.BaseOpenMonkeyMind.set_job_states)
    * [generic\_study\_data](#openmonkeymind._baseopenmonkeymind.BaseOpenMonkeyMind.generic_study_data)
    * [generic\_study\_data](#openmonkeymind._baseopenmonkeymind.BaseOpenMonkeyMind.generic_study_data)
    * [generic\_participant\_data](#openmonkeymind._baseopenmonkeymind.BaseOpenMonkeyMind.generic_participant_data)
    * [generic\_participant\_data](#openmonkeymind._baseopenmonkeymind.BaseOpenMonkeyMind.generic_participant_data)
    * [generic\_session\_data](#openmonkeymind._baseopenmonkeymind.BaseOpenMonkeyMind.generic_session_data)
    * [generic\_session\_data](#openmonkeymind._baseopenmonkeymind.BaseOpenMonkeyMind.generic_session_data)
    * [\_\_reduce\_\_](#openmonkeymind._baseopenmonkeymind.BaseOpenMonkeyMind.__reduce__)

<a id="openmonkeymind._baseopenmonkeymind"></a>

# openmonkeymind.\_baseopenmonkeymind

An instance of `BaseOpenMonkeyMind` lives as the `omm` object in the Python
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

<a id="openmonkeymind._baseopenmonkeymind.BaseJob"></a>

## BaseJob Objects

```python
class BaseJob()
```

A job consisting of a state, an id, and job/result variables.

A job consists of:
- A state, which can be PENDING, STARTED, or FINISHED.
- An id, which uniquely identifies the job. The id is not an index, i.e.,
  it does not indicate the position of the job in the job table.
- A set of job variables, such as experimental conditions.
- A set of result variables, such as response variables. A job can have
  multiple result variables if the job has been reset and then repeated. In
  that case, the last set of result variables is included.

<a id="openmonkeymind._baseopenmonkeymind.BaseJob.state"></a>

#### state

```python
@property
def state() -> int
```

The state of the job.

Returns
-------
int
    The state of the job (PENDING, STARTED, or FINISHED).

<a id="openmonkeymind._baseopenmonkeymind.BaseJob.id_"></a>

#### id\_

```python
@property
def id_() -> int
```

The unique identifier of the job.

Returns
-------
int
    The unique identifier of the job.

<a id="openmonkeymind._baseopenmonkeymind.BaseJob.finished"></a>

#### finished

```python
@property
def finished() -> bool
```

Indicates whether the job is finished.

Returns
-------
bool
    True if the job is finished, False otherwise.

<a id="openmonkeymind._baseopenmonkeymind.BaseJob.started"></a>

#### started

```python
@property
def started() -> bool
```

Indicates whether the job has started.

Returns
-------
bool
    True if the job has started, False otherwise.

<a id="openmonkeymind._baseopenmonkeymind.BaseJob.pending"></a>

#### pending

```python
@property
def pending() -> bool
```

Indicates whether the job is pending.

Returns
-------
bool
    True if the job is pending, False otherwise.

<a id="openmonkeymind._baseopenmonkeymind.BaseOpenMonkeyMind"></a>

## BaseOpenMonkeyMind Objects

```python
class BaseOpenMonkeyMind(object)
```

Allows for programmatic interaction with the OpenMonkeyMind server.

Lives as the `omm` object in the Python workspace in OpenSesame
experiments.

<a id="openmonkeymind._baseopenmonkeymind.BaseOpenMonkeyMind.current_participant"></a>

#### current\_participant

```python
@property
def current_participant() -> str
```

The identifier of the currently announced participant.

Returns
-------
str
    The identifier of the currently announced participant.

<a id="openmonkeymind._baseopenmonkeymind.BaseOpenMonkeyMind.current_alternate_participant_id"></a>

#### current\_alternate\_participant\_id

```python
@property
def current_alternate_participant_id() -> str
```

The alternate identifier of the currently announced participant.

Returns
-------
str
    The alternate identifier of the currently announced participant.

<a id="openmonkeymind._baseopenmonkeymind.BaseOpenMonkeyMind.current_participant_ids"></a>

#### current\_participant\_ids

```python
@property
def current_participant_ids() -> tuple(str, str)
```

A tuple with the participant identifier and the alternate participant identifier.

Returns
-------
tuple
    A tuple containing the participant identifier and the alternate
    participant identifier.

<a id="openmonkeymind._baseopenmonkeymind.BaseOpenMonkeyMind.current_participant_changed"></a>

#### current\_participant\_changed

```python
@property
def current_participant_changed() -> bool
```

Indicates whether a new participant identifier is available.

If this is true, the current participant is not automatically changed.
Rather, this property allows the system to check whether a new
participant would be identified if we would detect again.

Returns
-------
bool
    True if a new participant identifier is available, False otherwise.

<a id="openmonkeymind._baseopenmonkeymind.BaseOpenMonkeyMind.current_participant_name"></a>

#### current\_participant\_name

```python
@property
def current_participant_name() -> str
```

The name of the currently announced participant.

Returns
-------
str
    The name of the currently announced participant.

<a id="openmonkeymind._baseopenmonkeymind.BaseOpenMonkeyMind.participant_metadata"></a>

#### participant\_metadata

```python
@property
def participant_metadata() -> dict
```

A dict with metadata of the participant.

Returns
-------
dict
    A dictionary containing metadata of the participant.

<a id="openmonkeymind._baseopenmonkeymind.BaseOpenMonkeyMind.current_study"></a>

#### current\_study

```python
@property
def current_study() -> int
```

The id of the current study.

Returns
-------
int
    The id of the current study.

<a id="openmonkeymind._baseopenmonkeymind.BaseOpenMonkeyMind.current_job"></a>

#### current\_job

```python
@property
def current_job() -> int
```

The id of the current job.

This does not correspond to the position of the job in the job table.
For that, see `get_current_job_index()`.

Returns
-------
int
    The id of the current job.

<a id="openmonkeymind._baseopenmonkeymind.BaseOpenMonkeyMind.job_count"></a>

#### job\_count

```python
@property
def job_count() -> int
```

The number of jobs in the job table.

Returns
-------
int
    The number of jobs in the job table.

<a id="openmonkeymind._baseopenmonkeymind.BaseOpenMonkeyMind.connected"></a>

#### connected

```python
@property
def connected() -> bool
```

Indicates whether the client is connected to a server.

Returns
-------
bool
    True when connected to a server, False otherwise.

<a id="openmonkeymind._baseopenmonkeymind.BaseOpenMonkeyMind.available"></a>

#### available

```python
@property
def available() -> bool
```

Indicates whether a server appears to be available.

Returns
-------
bool
    True when a server appears to be available, False otherwise.

<a id="openmonkeymind._baseopenmonkeymind.BaseOpenMonkeyMind.announce"></a>

#### announce

```python
def announce(participant: str) -> Experiment
```

Announces a new participant and retrieves the experiment file for that participant.

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

<a id="openmonkeymind._baseopenmonkeymind.BaseOpenMonkeyMind.request_job"></a>

#### request\_job

```python
def request_job(job_index: int = None) -> BaseJob
```

Gets a job for the current experiment and participant.

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

<a id="openmonkeymind._baseopenmonkeymind.BaseOpenMonkeyMind.send_current_job_results"></a>

#### send\_current\_job\_results

```python
def send_current_job_results(job_results: dict)
```

Sends results for the current job.

This changes the current job status to FINISHED. There is now no current
job anymore.

Parameters
----------
job_results : dict
    A dictionary where keys are experimental variables, and values are values.

<a id="openmonkeymind._baseopenmonkeymind.BaseOpenMonkeyMind.get_current_job_index"></a>

#### get\_current\_job\_index

```python
def get_current_job_index() -> int
```

Gets the index of the current job in the job table.

This reflects the order of the job table and is therefore different
from the job id as provided by the `current_job` property.

Returns
-------
int
    The index of the current job in the job table.

<a id="openmonkeymind._baseopenmonkeymind.BaseOpenMonkeyMind.get_jobs"></a>

#### get\_jobs

```python
def get_jobs(from_index: int, to_index: int) -> list[BaseJob]
```

Gets all jobs between `from_index` and `to_index`.

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

<a id="openmonkeymind._baseopenmonkeymind.BaseOpenMonkeyMind.insert_jobs"></a>

#### insert\_jobs

```python
def insert_jobs(index: int, jobs: list[dict])
```

Inserts a list of jobs at the specified index.

The first job in the list has the specified index. The first job has
index 1. There is now no current job anymore.

Parameters
----------
index : int
    The index at which to insert the jobs.
jobs : list[dict]
    A list of dictionaries (not Job objects), where the variables and
    values are keys and values of the dict.

<a id="openmonkeymind._baseopenmonkeymind.BaseOpenMonkeyMind.delete_jobs"></a>

#### delete\_jobs

```python
def delete_jobs(from_index: int, to_index: int)
```

Deletes all jobs between `from_index` and `to_index`.

`to_index` is not included (i.e. Python-slice style). There is now no
current job anymore.

Parameters
----------
from_index : int
    The starting index (inclusive).
to_index : int
    The ending index (exclusive).

<a id="openmonkeymind._baseopenmonkeymind.BaseOpenMonkeyMind.set_job_states"></a>

#### set\_job\_states

```python
def set_job_states(from_index: int, to_index: int, state: int)
```

Sets the states of all jobs between `from_index` and `to_index`.

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

<a id="openmonkeymind._baseopenmonkeymind.BaseOpenMonkeyMind.generic_study_data"></a>

#### generic\_study\_data

```python
@property
def generic_study_data() -> object
```

General-purpose data specific to the current study but shared across all participants.

The data can be any object that can be serialized by JSON. If no data
has been set, it has the value `None`.

Returns
-------
object
    The general-purpose data specific to the current study.

<a id="openmonkeymind._baseopenmonkeymind.BaseOpenMonkeyMind.generic_study_data"></a>

#### generic\_study\_data

```python
@generic_study_data.setter
def generic_study_data(val: object)
```

Set the general-purpose data specific to the current study.

Parameters
----------
val : object
    The data to set. Must be serializable by JSON.

<a id="openmonkeymind._baseopenmonkeymind.BaseOpenMonkeyMind.generic_participant_data"></a>

#### generic\_participant\_data

```python
@property
def generic_participant_data() -> object
```

General-purpose data specific to the current participant but shared across all studies.

The data can be any object that can be serialized by JSON. If no data
has been set, it has the value `None`.

Returns
-------
object
    The general-purpose data specific to the current participant.

<a id="openmonkeymind._baseopenmonkeymind.BaseOpenMonkeyMind.generic_participant_data"></a>

#### generic\_participant\_data

```python
@generic_participant_data.setter
def generic_participant_data(val: object)
```

Set the general-purpose data specific to the current participant.

Parameters
----------
val : object
    The data to set. Must be serializable by JSON.

<a id="openmonkeymind._baseopenmonkeymind.BaseOpenMonkeyMind.generic_session_data"></a>

#### generic\_session\_data

```python
@property
def generic_session_data() -> object
```

General-purpose data specific to the current participant and study.

The data can be any object that can be serialized by JSON. If no data
has been set, it has the value `None`.

Returns
-------
object
    The general-purpose data specific to the current participant and study.

<a id="openmonkeymind._baseopenmonkeymind.BaseOpenMonkeyMind.generic_session_data"></a>

#### generic\_session\_data

```python
@generic_session_data.setter
def generic_session_data(val: object)
```

Set the general-purpose data specific to the current participant and study.

Parameters
----------
val : object
    The data to set. Must be serializable by JSON.

<a id="openmonkeymind._baseopenmonkeymind.BaseOpenMonkeyMind.__reduce__"></a>

#### \_\_reduce\_\_

```python
def __reduce__()
```

Avoids an error during unpickling.

Returns
-------
tuple
    A tuple to avoid unpickling errors.

