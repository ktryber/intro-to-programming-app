for note in concepts_1_1 and concepts_1_2:
			new_note = Notes_db(lesson_number = note[0])
			new_note.put()

			for note in your_notes:
    new_note = Notes_db(lesson_number = notes[0], title = notes[1], content = notes[2])
    new_note.put()