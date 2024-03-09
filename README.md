## 1. Penerapan Algortima Greedy
  Pada Algoritma bot game ini, kami menerapkan algoritma greedy dimana kami mengkonsiderasi pergerakan berdasarkan rasio point diamond terhadap jarak bot dari diamond (point/distance). Dari keseluruhan himpunan rasio, kami akan mengambil koordinat diamond dengan rasio terbesar dan menjadikan koordinat tersebut sebagai tujuan pergerakan bot.
## 2. Requirement Program
  Instalasi : 
  1. Node.js (https://nodejs.org/en) 
  2. Docker desktop (https://www.docker.com/products/docker-desktop/)
  3. yarn (cmd)
     ```
     npm install --global yarn
     ```
  Instalasi konfigurasi awal :
  1. Masuk ke folder src
  2. Download source code (.zip) pada [release game engine] https://github.com/haziqam/tubes1-IF2211-game-engine/releases/tag/v1.1.0
  3. Buka zip di dalam folder src
  4. Masuk ke directory dari game-engine
  6. Install dependencies menggunakan Yarn
     ```
     yarn
     ```
  7. Setup default environment variable dengan menjalankan script berikut untuk Windows
     ```
     ./scripts/copy-env.bat
     ```
  8. Setup local database (buka aplikasi docker desktop terlebih dahulu, lalu jalankan command berikut di terminal)
     ```
     docker compose up -d database
     ```
     ```
     ./scripts/setup-db-prisma.bat
     ```
  Build dan start :
     ```
     npm run build
     ```
     ```
     npm run start
     ```

## 3. Program Compiling
  1. Masuk ke directory src
  2. Untuk menjalankan satu bot dengan logic bot kita
     ```
     python main.py --logic Gacor --email=your_email@example.com --name=your_name --password=your_password --team etimo
     ```
  3. Untuk menjalankan beberapa bot sekaligus
     ```
     ./run-bots.bat
     ```
  4. Konfigurasi bot ada pada file run-bots.bat
## 4. Authors
1. Ibrahim Ihsan Rasyid - 13522018
2. Muhamad Rifki Virziadeili Harisman - 13522120
3. Muhammad Syarafi Akmal - 13522076
