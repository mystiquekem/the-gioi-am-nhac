"""Script to populate the database with sample Vietnamese instruments."""
from app import app, db, Instrument

def populate_sample_instruments():
    """Add sample instruments to the database."""
    
    instruments_data = [
        {
            'ID': 'dan-bau',
            'Name': 'Monochord',
            'Vietnamese_Name': 'Đàn bầu',
            'Category': 'String Instrument',
            'Region': 'Northern Vietnam',
            'Description': 'The đàn bầu is a Vietnamese monochord (one-string zither) with a unique, ethereal sound. It consists of a single string stretched over a wooden soundboard with a flexible rod attached to one end.',
            'History': 'Dating back to the 10th century, the đàn bầu has been an integral part of Vietnamese folk music. Originally used by blind street musicians, it gained popularity in royal courts during the Nguyễn Dynasty.',
            'Playing_Technique': 'The player plucks the string with one hand while bending the flexible rod with the other hand to create pitch variations. This technique produces the instrument\'s characteristic gliding, vibrato-rich tones.',
            'Audio_File': '/static/audio/dan-bau.mp3',
            'Video_URL': 'https://www.youtube.com/watch?v=example1',
            'Image_Main': '/static/images/instruments/dan-bau.jpg',
            'Image_Gallery': '[]'
        },
        {
            'ID': 'dan-tranh',
            'Name': 'Vietnamese Zither',
            'Vietnamese_Name': 'Đàn tranh',
            'Category': 'String Instrument',
            'Region': 'Southern Vietnam',
            'Description': 'The đàn tranh is a 16-string zither that is one of the most popular traditional Vietnamese instruments. It produces delicate, flowing melodies characteristic of Vietnamese music.',
            'History': 'Introduced to Vietnam from China around the 16th century, the đàn tranh was adapted to Vietnamese musical aesthetics. It became a staple in the đờn ca tài tử (southern amateur music) tradition.',
            'Playing_Technique': 'Players pluck the strings with their right hand while using their left hand to press down on the strings to create vibrato and bend pitches. The instrument is played while sitting with the instrument placed horizontally.',
            'Audio_File': '/static/audio/dan-tranh.mp3',
            'Video_URL': 'https://www.youtube.com/watch?v=example2',
            'Image_Main': '/static/images/instruments/dan-tranh.jpg',
            'Image_Gallery': '[]'
        },
        {
            'ID': 'dan-ti-ba',
            'Name': 'Vietnamese Lute',
            'Vietnamese_Name': 'Đàn tỳ bà',
            'Category': 'String Instrument',
            'Region': 'Central Vietnam (Huế)',
            'Description': 'The đàn tỳ bà is a pear-shaped lute with four strings, adapted from the Chinese pipa. It has a rich, resonant sound and is used in both solo and ensemble performances.',
            'History': 'Brought to Vietnam during Chinese cultural exchanges, the đàn tỳ bà became particularly prominent in the royal court music of Huế. It was refined by Vietnamese musicians to suit local musical tastes.',
            'Playing_Technique': 'Held vertically on the lap, the player uses various plucking techniques including tremolo, harmonics, and percussive strikes on the soundboard to create a wide range of tones and effects.',
            'Audio_File': '/static/audio/dan-ti-ba.mp3',
            'Video_URL': 'https://www.youtube.com/watch?v=example3',
            'Image_Main': '/static/images/instruments/dan-ti-ba.jpg',
            'Image_Gallery': '[]'
        },
        {
            'ID': 'sao-truc',
            'Name': 'Bamboo Flute',
            'Vietnamese_Name': 'Sáo trúc',
            'Category': 'Wind Instrument',
            'Region': 'Throughout Vietnam',
            'Description': 'The sáo trúc is a transverse bamboo flute with six finger holes. Simple in construction but capable of expressing complex emotions, it is beloved in Vietnamese folk music.',
            'History': 'Used for centuries by farmers and shepherds, the sáo trúc represents the pastoral traditions of Vietnam. It remains popular in both traditional and contemporary Vietnamese music.',
            'Playing_Technique': 'Blown across an embouchure hole while covering and uncovering finger holes to produce different notes. Advanced players use breath control and partial hole-covering to create quarter tones and ornamentations.',
            'Audio_File': '/static/audio/sao-truc.mp3',
            'Video_URL': 'https://www.youtube.com/watch?v=example4',
            'Image_Main': '/static/images/instruments/sao-truc.jpg',
            'Image_Gallery': '[]'
        },
        {
            'ID': 'ken-bau',
            'Name': 'Gourd Oboe',
            'Vietnamese_Name': 'Kèn bầu',
            'Category': 'Wind Instrument',
            'Region': 'Southern Vietnam',
            'Description': 'The kèn bầu is a unique free-reed instrument made from a dried gourd and bamboo pipes. It has a distinctive, buzzing sound that is instantly recognizable.',
            'History': 'Originating from the Khmer communities in southern Vietnam, the kèn bầu is traditionally used in ceremonial music and festivals. It represents the cultural diversity of Vietnamese music.',
            'Playing_Technique': 'Air is blown into the gourd chamber, causing metal reeds in the bamboo pipes to vibrate. Players can create different pitches by opening and closing finger holes on the pipes.',
            'Audio_File': '/static/audio/ken-bau.mp3',
            'Video_URL': 'https://www.youtube.com/watch?v=example5',
            'Image_Main': '/static/images/instruments/ken-bau.jpg',
            'Image_Gallery': '[]'
        },
        {
            'ID': 'trong-com',
            'Name': 'Rice Drum',
            'Vietnamese_Name': 'Trống cơm',
            'Category': 'Percussion Instrument',
            'Region': 'Northern Vietnam',
            'Description': 'The trống cơm is a small barrel drum with two heads, traditionally used in folk music ensembles. Its name means "rice drum" due to its shape resembling a rice container.',
            'History': 'Used in Vietnamese villages for centuries, the trống cơm provides rhythmic foundation in traditional music. It is essential in quan họ (northern folk songs) accompaniment.',
            'Playing_Technique': 'Played with bare hands or wooden sticks, striking different parts of the drum heads to produce various tones. The drum can be held or placed on a stand.',
            'Audio_File': '/static/audio/trong-com.mp3',
            'Video_URL': 'https://www.youtube.com/watch?v=example6',
            'Image_Main': '/static/images/instruments/trong-com.jpg',
            'Image_Gallery': '[]'
        }
    ]
    
    with app.app_context():
        # Clear existing instruments (optional)
        # db.session.query(Instrument).delete()
        
        for data in instruments_data:
            # Check if instrument already exists
            existing = db.session.get(Instrument, data['ID'])
            if existing:
                print(f"Instrument {data['ID']} already exists, skipping...")
                continue
            
            instrument = Instrument(**data)
            db.session.add(instrument)
            print(f"Added instrument: {data['Vietnamese_Name']} ({data['Name']})")
        
        db.session.commit()
        print(f"\nSuccessfully populated {len(instruments_data)} instruments!")

if __name__ == '__main__':
    populate_sample_instruments()