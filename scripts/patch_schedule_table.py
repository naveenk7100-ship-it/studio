with open('docs/review/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace('\r\n', '\n')

old_tbl = """                        <tr style="background: rgba(0, 229, 255, 0.08);">
                            <td><strong>TODAY • Slot 1</strong><br><small style="color:var(--text-secondary)">12:30 PM IST</small></td>
                            <td><strong>wheresryan22 / anatomy</strong><br><small style="color:var(--accent-cyan)">25,676 Stars • MIT</small></td>
                            <td><span class="badge-ready" style="font-size:11px; padding:3px 8px;">READY</span></td>
                        </tr>
                        <tr style="background: rgba(255, 183, 3, 0.08);">
                            <td><strong>TODAY • Slot 2</strong><br><small style="color:var(--text-secondary)">8:30 PM IST</small></td>
                            <td><strong>browser-use / browser-use</strong><br><small style="color:var(--accent-orange)">120,244 Stars • MIT</small></td>
                            <td><span class="badge-ready" style="font-size:11px; padding:3px 8px;">READY</span></td>
                        </tr>"""

new_tbl = """                        <tr style="background: rgba(0, 229, 255, 0.08);">
                            <td><strong>PILLAR A • Slot 1</strong><br><small style="color:var(--text-secondary)">12:30 PM IST</small></td>
                            <td><strong>How ChatGPT Works in 3D</strong><br><small style="color:var(--accent-cyan)">NeurIPS arXiv:1706.03762 • OpenAI Tech Reports</small></td>
                            <td><span class="badge-ready" style="font-size:11px; padding:3px 8px;">READY</span></td>
                        </tr>
                        <tr style="background: rgba(226, 184, 120, 0.08);">
                            <td><strong>PILLAR B • Slot 2</strong><br><small style="color:var(--text-secondary)">8:30 PM IST</small></td>
                            <td><strong>Best Tool: PDF Paper Summarization</strong><br><small style="color:var(--accent-orange)">pypdfium2 (Google C++) • 59ms Benchmark</small></td>
                            <td><span class="badge-ready" style="font-size:11px; padding:3px 8px;">READY</span></td>
                        </tr>
                        <tr style="background: rgba(255, 255, 255, 0.02);">
                            <td><strong>PILLAR C • Slot 3</strong><br><small style="color:var(--text-secondary)">Next Slot</small></td>
                            <td><strong>Real-Life Playbook</strong><br><small style="color:var(--text-secondary)">Production Architecture Recipe</small></td>
                            <td><span style="font-size:11px; padding:3px 8px; color:var(--text-secondary);">QUEUED</span></td>
                        </tr>
                        <tr style="background: rgba(255, 255, 255, 0.02);">
                            <td><strong>PILLAR D • Slot 4</strong><br><small style="color:var(--text-secondary)">Next Slot</small></td>
                            <td><strong>Fresh Drop</strong><br><small style="color:var(--text-secondary)">Daily Intelligence 6h Scan (&le; 48h / &le; 14d)</small></td>
                            <td><span style="font-size:11px; padding:3px 8px; color:var(--text-secondary);">QUEUED</span></td>
                        </tr>"""

old_tbl = old_tbl.replace('\r\n', '\n')
new_tbl = new_tbl.replace('\r\n', '\n')

if old_tbl in text:
    text = text.replace(old_tbl, new_tbl)
    with open('docs/review/index.html', 'w', encoding='utf-8') as f:
        f.write(text)
    print('Schedule table updated successfully!')
else:
    print('Target table not found!')
