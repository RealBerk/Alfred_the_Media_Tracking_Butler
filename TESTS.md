Alfred Media Tracker Butler Test Senaryolari

#	Senaryo---Input---Beklenen---Olan----Durum
1	Kaydedilen Bilgileri geri yukleme----Bir kere calistirildiktan sonra yeniden baslatildi----Onceki bilgileri hatirlamasi---Hatirladi---Pass
2	Hatali input	----()Bos karakter veya beklenmeyen karakterler----Hata verir ve yeniden input istenir----Yeniden input istedi	Pass
3	Gecersiz yil veya medya turu-----Gecersiz input girildi----(abcd yil olarak) ve Listelenmeyen tur numarasi-----Hata verir ve yeniden input istenir----Hata verdi ve yeniden input istedi----Pass
4	Export normal kullanim----Export fonksiyonu dosya yazabilmesi	----Kaydedilen listeleri text dosyasina yazar----Text dosyasi uretildi ve icerik dogru----Pass
5	Reset iptali	Baslanilan reset islemi iptali----RESET yazilmadiginda islemi iptal eder----Islem iptal edildi ve kaydedilen bilgiler silinmedi----Pass

