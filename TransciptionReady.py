import assemblyai as aai
def timestamps_to_milisekonds(timestamp):
   print('t=',timestamp)
   if timestamp[0:2]=='00':
       print(timestamp[0:2])
       hours=0
   else:
       print('eslse',timestamp[0:2])
       print(timestamp[0:2])
       if timestamp[1]!=':':
           hours = int(timestamp[0:2])
       else:
           hours=int(timestamp[0])




   minutes = int(timestamp[3:5])
   sekonds = int(timestamp[6:8])
   milisecond = int(timestamp[9:len(timestamp)])
   # print(hours,minutes,sekonds,milisecond)
   miliseconds = milisecond + sekonds * 1000 + minutes * 1000 * 60 + hours * 1000 * 60 * 60
   return miliseconds




def miliseconds_to_timestamps(milisecond):
   hours = int(milisecond // (1000 * 60 * 60))
   if hours // 10 == 0:
       hours = f'0{int(hours)}'
   minutes = (milisecond % (1000 * 60 * 60)) // (1000 * 60)
   if minutes // 10 == 0:
       minutes = f'0{int(minutes)}'
   seconds = int(((milisecond % (1000 * 60 * 60)) % (1000 * 60)) // 1000)
   if seconds // 10 == 0:
       seconds = f'0{int(seconds)}'
   milisecond = int(((milisecond % (1000 * 60 * 60)) % (1000 * 60)) % 1000)
   milisecond=f'{milisecond}'
   if len(milisecond)<3:
       milisecond=milisecond+'0'
   timestamp = f'{hours}:{minutes}:{seconds},{milisecond}'
   return timestamp
def create_transcribe(FILE_URL,duration,language):
   aai.settings.api_key = f"899ee1d7821d4483b7d9c95984234a3c"
   config = aai.TranscriptionConfig(language_code=language)
   transcriber = aai.Transcriber(config=config)
   transcript = transcriber.transcribe(FILE_URL)
   sent=transcript.get_sentences()
   sentences=[]
   starts=[]
   ends=[]
   for x in sent:
       sentences.append(x.text)
       starts.append(x.start)
       ends.append(x.end)


   # if starts[0]-600>=0:
   #     finst=[starts[0]-600]
   # else:
   #     finst=[0]
   # actual_start=starts[0]
   # finend=[]
   # finsent=[]
   # new=False
   # temp=sentences[0]
   # for i in range(1,len(sentences)):
   #     start=starts[i]
   #     end=ends[i]
   #     anterior_bosh=start-ends[i-1]
   #     if i!=len(sentences)-1:
   #         next_sent=sentences[i+1]
   #         next_bosh=starts[i+1]-end
   #     else:
   #         next_bosh=duration
   #         next_sent=''
   #     print(sentences[i])
   #     print(f'temp={temp}')
   #     temp=str(temp)+str(sentences[i])+' '
   #     if new and anterior_bosh>600:
   #         actual_start=start-600
   #         finst.append(start-600)
   #         new=False
   #     elif new and anterior_bosh<=600:
   #         finst.append(starts[i-1]+100)
   #         actual_start=starts[i-1]+100
   #         new=False
   #     if len(temp+next_sent)>55 or next_bosh>=1000 or end==ends[len(sentences)-1]:
   #         finsent.append(temp)
   #         temp=''
   #         if next_bosh>=1100 and end-actual_start<7000:
   #             finend.append(end+1000)
   #         elif end-actual_start>=7000:
   #             finend.append(actual_start+7000)
   #         else:
   #             finend.append(end+next_bosh-100)
   #         new=True
   #
   #
   #
   #
   #
   #
   #
   #






   return starts,ends,sentences

