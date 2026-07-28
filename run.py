import sys
import os

# เพิ่มโฟลเดอร์ src เข้าไปใน path เพื่อให้ Python มองเห็น package chatbridge
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from chatbridge.main import main

if __name__ == '__main__':
    main()
