from __future__ import annotations

from types import MappingProxyType

GLOSSARY = MappingProxyType(
    {
        "Batch": "The batch system, e.g. PBS, LSF, SLURM, SGE, HTCondor, etc.",
        "CE": "Computing Element",
        "CLI": "Command Line Interface",
        "DICE": "Data Intensive Computing Environment",
        "FTS": "File Transfer Service",
        "HDFS": "Hadoop Distributed File System",
        "scheduler": "The node that schedules jobs for the batch system (see 'dice info schedulers')",
        "SE": "Storage Element",
        "worker node": "the node that executes the batch job (see 'dice info workers')",
    }
)
