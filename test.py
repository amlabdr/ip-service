def calculate_differences():
    with open('start_timestamps.txt', 'r') as start_file, open('end_timestamps.txt', 'r') as end_file, open('delta.txt', 'w') as delta_file:
        start_lines = start_file.readlines()
        end_lines = end_file.readlines()

        if len(start_lines) != len(end_lines):
            print("Error: The number of start times and end times doesn't match.")
            return

        differences = []
        for start_time, end_time in zip(start_lines, end_lines):
            start_time = float(start_time.strip())
            end_time = float(end_time.strip())
            difference = end_time - start_time
            differences.append(difference)
            delta_file.write(f'{difference}\n')

        average_difference = sum(differences) / len(differences) if len(differences) > 0 else 0

    return average_difference
diff = calculate_differences()
print(diff)
print("rate = ",1/diff)

xml_header = '''<rpc xmlns="urn:ietf:params:xml:ns:netconf:base:1.0" message-id="1">
  <edit-config>
    <target>
      <running/>
    </target>
    <config>
      <!-- Configuration data goes here -->
    </config>
  </edit-config>
</rpc>'''

byte_count = len(xml_header.encode('utf-8'))
print(f"Number of bytes in XML header: {byte_count}")
