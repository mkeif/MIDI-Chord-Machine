import time
import rtmidi

chords_list = ["maj7", "min7", "maj9", "min9", "Dom7"]
chord_formula = {"maj7":"434", "min7":"343", "maj9":"434", "min9":"3434", "Dom7": "333"}

oct = 3

NOTES = ['C', 'C#', 'D', 'Eb', 'E', 'F', 'F#', 'G', 'Ab', 'A', 'Bb', 'B']
OCTAVES = list(range(11))
NOTES_IN_OCTAVE = len(NOTES)

errors = {
    'notes': 'Bad input, please refer this spec-\n'
}
class MIDIplayer:
    def __init__(self):
        out = rtmidi.MidiOut()
        self.out = out
        self.on = []
        self.current = (0, 0)
        self.out.open_port(0)
        print(self.out)
        
        
    def swap_accidentals(self, note):
        if note == 'Db':
            return 'C#'
        if note == 'D#':
            return 'Eb'
        if note == 'E#':
            return 'F'
        if note == 'Gb':
            return 'F#'
        if note == 'G#':
            return 'Ab'
        if note == 'A#':
            return 'Bb'
        if note == 'B#':
            return 'C'

        return note

    def note_to_number(self, note, octave) -> int:
        if type(note) == int:
            return note
        
        note = self.swap_accidentals(note)
        assert note in NOTES, errors['notes']
        assert octave in OCTAVES, errors['notes']

        note = NOTES.index(note)
        note += (NOTES_IN_OCTAVE * octave)

        assert 0 <= note <= 127, errors['notes']

        return note
    
    def formula_to_chord(self,note, chord):
        #this function returns the chord type depending on what number is passed.
        a = []
        sum = 0
        ind = self.note_to_number(note, oct)
        
        
        for i in chord:
            n = int(i)
            sum = sum + n
            
            step = ind + sum
            
            a.append(step)
     
        return a
            
            
    
    def sendsignal(self, note):
        notenumber = self.note_to_number(note, oct)
        self.out.send_message([0x90, notenumber, 100])  ##add signal parameters
        
            
        self.on.append(note)
        
    def offall(self):
        for i in self.on:
            notenumber = self.note_to_number(i, oct)
            self.out.send_message([0x80, notenumber , 0]) #add exact signal parameters
    
    def play(self, note, fingers):
        if self.current != (note, fingers) :
            self.offall()
            
            if fingers > 4:
                fingers = 4
            chord = chords_list[fingers]
            chord = chord_formula[chord]
            
            notes = self.formula_to_chord(note, chord)
            
            #print(note)
            #print(fingers)
            
            for i in notes:
                print(i, end = " ")   
                self.sendsignal(i)
            print()
        
        
        
        self.current = (note, fingers)



#while True:
    
    #note_on = [0x90, 49, 100]
    #note_off = [0x80, 49, 0]
   # midiout.send_message(note_on)
   # time.sleep(1.0)
   # midiout.send_message(note_off)
    #time.sleep(0.1)
  