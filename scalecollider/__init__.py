from typing import List
from itertools import product


def get_diatonic_intervals() -> List[List[int]]:
    # A 'valid interval' is a combination of whole-and-half steps which adds up to 1 octave (12 steps)
    # Question: Does every scale need to have one of each note? Can a pentatonic scale be a key?
    # Question: Does every scale end on the octave?
    diatonic_intervals = []
    # Find all combinations of a whole step & half step with 7 notes
    all_step_combinations = [x for x in product([1, 2], repeat=7)]
    for interval in all_step_combinations:
        # A valid interval
        if sum(interval) == 12:
            diatonic_intervals.append([int(x) for x in interval])

    print(f'Found {len(diatonic_intervals)} diatonic intervals in {len(all_step_combinations)} step combinations')
    return diatonic_intervals


class Scale:
    # Keep track of the names which can be used to refer to a particular pitch when building a scale
    _ENHARMONIC_NOTES = {
        0: ['A', 'G##', 'Bbb', 'Cbbb'],
        1: ['A#', 'Bb', 'G###', 'Cbb'],
        2: ['B', 'A##', 'Cb', 'Dbbb'],
        3: ['C', 'B#', 'A###', 'Dbb'],
        4: ['C#', 'B##', 'Db', 'Ebbb'],
        5: ['D', 'C##', 'B###', 'Ebb', 'Fbbb'],
        6: ['D#', 'Eb', 'C###', 'Fbb'],
        7: ['E', 'D##', 'Fb', 'Gbbb'],
        8: ['F', 'E#', 'D###', 'Gbb'],
        9: ['F#', 'E##', 'Gb', 'Abbb'],
        10: ['G', 'F##', 'E###', 'Abb'],
        11: ['G#', 'Ab', 'F###', 'Bbbb']
    }

    # Used to know which note must come 'in sequence' after another note
    _NOTE_ORDER = ['A', 'B', 'C', 'D', 'E', 'F', 'G']

    def __init__(self, root_note: str, interval: List[int]) -> None:
        self.root_note = root_note
        self.interval = interval
        self.notes = self._generate_scale(root_note, interval)

    @classmethod
    def get_all_note_names(cls):
        """Return every possible note which is suitable as the root note of a key.
        """
        # For now, returns every known name for every pitch
        all_possible_notes = [x for sublist in cls._ENHARMONIC_NOTES.values() for x in sublist]
        return all_possible_notes

    def _next_note(self, prev_note: str) -> str:
        """Find the next letter-note name in the scale, after prev_note.
        """
        fundamental = prev_note[0]
        idx = self._NOTE_ORDER.index(fundamental) + 1
        # Wrap around to A if we've gone past G
        idx %= len(self._NOTE_ORDER)
        return self._NOTE_ORDER[idx]

    @classmethod
    def _note_num_from_name(cls, note_name: str) -> int:
        for num, enharmonic_notes in cls._ENHARMONIC_NOTES.items():
            if note_name in enharmonic_notes:
                return num
        raise RuntimeError(f'Unknown note {note_name}')

    def _generate_scale(self, starting_note: str, scale_interval: List[int]) -> List[str]:
        # Determine the pitch indexes which will be used in the scale, based on the provided interval & root note
        scale_note_indexes = []
        curr_idx = self._note_num_from_name(starting_note)
        for interval in scale_interval:
            scale_note_indexes.append(curr_idx)
            curr_idx += interval

        # The scale will always start on the provided note
        scale_notes = [starting_note]
        for idx, note_idx in enumerate(scale_note_indexes[1:]):
            # Wrap around to A if we've gone past G#
            note_idx %= 12
            previous_note = scale_notes[idx]

            # What can we call the next pitch in the scale?
            possible_note_names = self._ENHARMONIC_NOTES[note_idx]
            # Get the enharmonically-equivalent note name which fits the rule that there must be 7 letter notes
            next_note_letter = self._next_note(previous_note)
            for note_name in possible_note_names:
                if note_name.startswith(next_note_letter):
                    scale_notes.append(note_name)
                    break
            else:
                raise RuntimeError(f'Needed a {next_note_letter} ({previous_note} + interv) '
                                   f'in {starting_note} {scale_interval}: {", ".join(scale_notes)}')
        scale_notes.append(starting_note)
        return scale_notes

    def has_same_notes(self, other: 'Scale') -> bool:
        return sorted(self.notes) == sorted(other.notes)

    def __repr__(self):
        formatted_scale = ' '.join(['{:4}'.format(note) for note in self.notes])
        formatted_note = '{:4}'.format(self.root_note)
        return f'{formatted_note} @ {formatted_scale}'


if __name__ == '__main__':
    seen_scales = []

    diatonic_intervals = get_diatonic_intervals()
    all_root_notes = Scale.get_all_note_names()
    print(f'Generating scales from {len(all_root_notes)} enharmonic root notes...')
    for diatonic_interval in diatonic_intervals:
        for note in all_root_notes:
            # print(f'Producing scale with interval{diatonic_interval} @ {note}...')
            try:
                seen_scales.append(Scale(note, diatonic_interval))
            except RuntimeError as e:
                # Uncomment this to see scales that can't be produced with our enharmonically-equivalent pitch def.
                # print(f'Scale is impossible: {str(e)}')
                pass
    print(f'Generated {len(seen_scales)} scales')

    collisions = []
    for scale1 in seen_scales:
        for scale2 in seen_scales:
            # Don't check a scale against itself
            if scale1 == scale2:
                continue

            if scale1.has_same_notes(scale2):
                print(f'Found collision!\nScale 1: {scale1}\nScale 2: {scale2}')
                collisions.append((scale1, scale2))

    print(f'Found {len(collisions)} collisions')
