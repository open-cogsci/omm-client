
=====================================================
plugins/omm_conditionner
=====================================================

- "Number of pulses" and "Pause between pulses" don’t seem to be used as such by ‘SeedDispenser’, which simply works with a duration in seconds.
If that’s the case, we can remove "Pause between pulses" and  use a common duration setting for both the SeedDispenser and JuiceDispenser

- Is the 'reward' and juice checkbox are really necessary? . I vote to remove it. (The dropdown list is sufficient, isn’t it? )

- JuicePumpCdp => Do you really need the strings to start and stop the pump to be configurable? If not, it would be better to hardcode them in the file to avoid cluttering the interface.
