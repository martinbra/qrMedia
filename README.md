# qrMedia
play your media with the help of some qrcode.

## Scripts

### qrcode_generator.py
pass a range to generate_range to create a list of qrcodes files:
```
# Generate range 0-9:
file_range = range(10)

# saves to qrcodes/*.png
generate_range(file_range)
```

## TODO'S:

- [ ] Graphical interface for qrcode_generator.py
- [ ] Read from csv/xlsx file
- [ ] Database generator to store created pairs qrcode:link
- [ ] Desktop program (win/linux/web?) to read qrcode and play media
- [ ] Android/iOS app to read qrcode and open media
