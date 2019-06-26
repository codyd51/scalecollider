scalecollider
----------

While going over music-theory basics with my guitar teacher, he explained how to interpret the key signature of sheet music.

A key signature is a list of sharp and flat notes placed at the beginning of sheet music. My teacher explained that, as every key of the
major scale has a unique combination of sharp and flat notes, you can read the key signature to find out which key you're in.

I asked him if this rule holds true for any scale: that is, does every possible scale have some unique combination of sharp and flat notes?
If not, how many unique combinations are there?

Let's find out!

*scalecollider* is a Python experiment to answer this question. It does this:

* Generate every diatonic scale interval
    * A diatonic scale is a pattern of 7 half steps/whole steps, which add up to an octave.
    * For example, one diatonic scale interval, the major scale, is this sequence: [2, 2, 1, 2, 2, 2, 1]
    * There are 21 possible diatonic scale intervals
    
* For every diatonic scale interval, generate each key of that scale by counting out the scale interval from every possible note

* Keep track of every scale that gets generated

* Remove duplicates

Results
------------

- 21 possible diatonic scale intervals (major scale pattern, minor scale pattern, 19 others)

- 861 possible scales from these, if scales rooted on triple-sharps and triple-flats are included

- 123 unique combinations of notes which form a scale, if scales rooted on triple-sharps and triple-flats are included

Questions
------------

123 seems like an arbitrary number, and I'm still trying to figure out the intuition for why this is what it is.

Intuitively, it feels like the answer should be some multiple of 12.

This project only deals with diatonic scales, but there are many more possible scales / scale patterns if you remove the requirement 
that a scale must contain one of each letter-note. Additionally, it may be possible, though perhaps unwise, to use a scale
which does not fit perfectly into an octave.

License
------------

MIT
