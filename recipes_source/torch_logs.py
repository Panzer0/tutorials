"""
(beta) Using TORCH_LOGS python API with torch.compile
==========================================================================================
**Author:** `Michael Lazos <https://github.com/mlazos>`_
"""

import logging

######################################################################
#
# This tutorial introduces the ``TORCH_LOGS`` environment variable, as well ass the Python API, and
# demonstrates how to apply it to observe the phases  of ``torch.compile``.
#
# .. note::
#
#   This tutorial requires PyTorch 2.2.0 or later.
#
#


######################################################################
# Setup
# ~~~~~~~~~~~~~~~~~~~~~
# In this example, we'll set up a simple Python function which performs an elementwise
# add and observe the compilation process with ``TORCH_LOGS`` Python API.
#
# .. note::
#
#   There is also an environment variable ``TORCH_LOGS``, which can be used to
#   change logging settings at the commandline. The equivalent environment
#   variable setting is shown for each example.

import torch


@torch.compile()
def fn(x, y):
    z = x + y
    return z + 2


inputs = (torch.ones(2, 2, device="cuda"), torch.zeros(2, 2, device="cuda"))


# print separator and reset dynamo
# between each example
def separator(name):
    print(f"==================={name}=========================")
    torch._dynamo.reset()


separator("Dynamo Tracing")
# View dynamo tracing
# TORCH_LOGS="+dynamo"
torch._logging.set_logs(dynamo=logging.DEBUG)
fn(*inputs)

separator("Traced Graph")
# View traced graph
# TORCH_LOGS="graph"
torch._logging.set_logs(graph=True)
fn(*inputs)

separator("Fusion Decisions")
# View fusion decisions
# TORCH_LOGS="fusion"
torch._logging.set_logs(fusion=True)
fn(*inputs)

separator("Output Code")
# View output code generated by inductor
# TORCH_LOGS="output_code"
torch._logging.set_logs(output_code=True)
fn(*inputs)

separator("")

######################################################################
# Conclusion
# ~~~~~~~~~~
#
# In this tutorial we introduced the TORCH_LOGS environment variable and python API
# by experimenting with a small number of the available logging options.
# To view descriptions of all available options, run any python script
# which imports torch and set TORCH_LOGS to "help".
#
# Alternatively, you can view the `torch._logging documentation`_ to see
# descriptions of all available logging options.
#
# .. _torch._logging documentation: https://pytorch.org/docs/main/logging.html
