@echo off
powershell -ExecutionPolicy Bypass -File "C:\Users\maste\.openclaw\workspace\x.ps1" -c "%*" > "C:\Users\maste\.openclaw\workspace\x.txt" 2>&1
type "C:\Users\maste\.openclaw\workspace\x.txt"
