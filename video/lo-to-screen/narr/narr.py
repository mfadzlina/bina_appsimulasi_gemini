import json, esp
N=[
"El O tu Skrin, ialah satu proses yang membantu pendidik membina video pengajaran secara lebih terancang, bermula dengan objektif pembelajaran, dan bukannya terus menghasilkan prompt E-ai.",
"Perjalanan ini bermula dengan Lerning Autkam, atau El O. Kita perlu jelas terlebih dahulu. Selepas menonton video ini, apakah perkara yang pelajar sepatutnya tahu, faham, atau boleh lakukan?",
"Selepas El O ditentukan, kita memilih Visyual Evidens. Iaitu visual yang paling jelas, untuk membantu pelajar melihat dan memahami konsep. Bukan sekadar mencantikkan video, tetapi visual yang benar benar menyokong pembelajaran.",
"Seterusnya, kita menentukan strategi pengajaran yang sesuai. Adakah kita mahu menerangkan konsep, membandingkan dua keadaan, menunjukkan sesuatu proses, atau menyelesaikan satu masalah?",
"Daripada strategi tersebut, kita membina Sin Map. Kandungan dipecahkan kepada beberapa sin pendek, supaya setiap sin mempunyai satu fokus yang jelas. Untuk video Gugel Flo, satu sin biasanya sekitar lapan saat.",
"Dalam proses ini, E-ai bukan sekadar untuk menghasilkan video. Kita menggunakan E-ai Cekpoin, untuk berbincang, menyemak, dan memperhalusi keputusan pengajaran, sebelum bergerak ke langkah seterusnya.",
"Selepas Sin Map siap, kita memastikan kontinuiti antara setiap sin. Watak, persekitaran, arah visual, dan gaya persembahan perlu konsisten, supaya video terasa seperti satu perjalanan pembelajaran yang lengkap, bukannya klip yang terpisah.",
"Barulah kita masuk ke peringkat Gugel Flo, di mana setiap sin dijana satu demi satu, berdasarkan perancangan yang telah dibuat.",
"Klip yang siap kemudian dibawa ke proses editing, contohnya menggunakan Kepkat. Di sinilah kita menambah suara latar, kapsyen, overle, dan animasi, yang membantu pelajar memberi perhatian kepada perkara penting.",
"Akhirnya, kita memperoleh sebuah video Pe De Pe yang siap digunakan.",
"Jadi, El O tu Skrin sebenarnya bukan sekadar proses menghasilkan video menggunakan E-ai. Ia ialah satu cara berfikir.",
"Bermula dengan apa yang pelajar perlu belajar, menentukan bagaimana mereka perlu melihatnya, kemudian barulah memilih bagaimana E-ai boleh membantu kita menghasilkan pengalaman pembelajaran tersebut.",
"Daripada Ai-dia, kepada Plen, Kri-eit, Tiic, dan akhirnya, Impek.",
"Video mungkin pendek, tetapi apabila perancangannya tepat, impaknya kepada pembelajaran boleh menjadi jauh lebih besar.",
"Video kecil, impak besar.",
]
d=[round(esp.synth(t,f'narr/{i:02d}.wav',voice='ms+f3',rate=148,pitch=52),2) for i,t in enumerate(N)]
json.dump(d,open('narr/durs.json','w')); print(d, sum(d))
