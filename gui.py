from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtWidgets import QWidget, QTextEdit, QComboBox, QLabel, QSlider, QPushButton, QStatusBar, QHBoxLayout, QVBoxLayout
from synthesizer import Synthesizer


class GUI(QWidget):
	def __init__(self):
		super(GUI, self).__init__()
		self.setWindowTitle("Abjad TTS")
		self.setWindowIcon(QIcon("images/arabic.png"))
		self.resize(1024, 768)

		# layout
		self.h0_layout = QHBoxLayout()
		self.h4_layout = QHBoxLayout()
		self.h1_layout = QHBoxLayout()
		self.h2_layout = QHBoxLayout()
		self.h3_layout = QHBoxLayout()
		self.all_v_layout = QVBoxLayout()

		# widgets
		self.text_edit = QTextEdit(self) # h0
		self.synthesize_button = QPushButton("Generate", self) # h1
		self.checkpoint_combo = QComboBox(self)
		self.play_pause_btn = QPushButton(self) # h2
		self.progress_slider = QSlider(Qt.Horizontal, self)
		self.time_label = QLabel(self)
		self.sound_btn = QPushButton(self) # h3
		self.volume_slider = QSlider(Qt.Horizontal, self)
		self.status_bar = QStatusBar(self) # h4

		self.player = QMediaPlayer(self)
		self.synthesizer = Synthesizer()

		self.widget_init()
		self.layout_init()
		self.signal_init()

	def widget_init(self):
		self.text_edit.setFont(QFont("Arial", 16))
		self.status_bar.showMessage("Welcome! Try out my Abjad-VITS & MMS-TTS by Meta in Arabic and Hebrew.")
		self.synthesize_button.setFont(QFont("Arial", 12))
		self.synthesize_button.setFixedSize(128, 80)
		self.checkpoint_combo.setFont(QFont("Arial", 12))
		self.checkpoint_combo.setFixedHeight(40)
		self.checkpoint_combo.addItem(" Abjad-VITS-ara") # a space added before every option to make GUI more beautiful
		self.checkpoint_combo.addItem(" Abjad-VITS-heb")
		self.checkpoint_combo.addItem(" MMS-TTS-ara")
		self.checkpoint_combo.addItem(" MMS-TTS-heb")
		self.play_pause_btn.setIcon(QIcon("images/play.png"))
		self.play_pause_btn.setFixedSize(48, 48)
		self.progress_slider.setEnabled(False)
		self.time_label.setText("--/--")
		self.sound_btn.setIcon(QIcon("images/sound_on.png"))
		self.sound_btn.setFixedSize(48, 48)
		self.volume_slider.setRange(0, 100)
		self.volume_slider.setValue(100)

	def layout_init(self):
		self.h0_layout.addWidget(self.text_edit)
		self.h1_layout.addWidget(self.synthesize_button)
		self.h1_layout.addWidget(self.checkpoint_combo)
		self.h2_layout.addWidget(self.play_pause_btn)
		self.h2_layout.addWidget(self.progress_slider)
		self.h2_layout.addWidget(self.time_label)
		self.h3_layout.addWidget(self.sound_btn)
		self.h3_layout.addWidget(self.volume_slider)
		self.h4_layout.addWidget(self.status_bar)

		self.all_v_layout.addLayout(self.h0_layout)
		self.all_v_layout.addLayout(self.h1_layout)
		self.all_v_layout.addLayout(self.h2_layout)
		self.all_v_layout.addLayout(self.h3_layout)
		self.all_v_layout.addLayout(self.h4_layout)
		self.setLayout(self.all_v_layout)

	def signal_init(self):
		self.sound_btn.clicked.connect(self.sound_btn_func)
		self.play_pause_btn.clicked.connect(self.play_pause_btn_func)
		self.volume_slider.valueChanged.connect(self.volume_slider_func)
		self.player.durationChanged.connect(self.get_duration_func)
		self.player.positionChanged.connect(self.get_position_func)
		self.progress_slider.sliderMoved.connect(self.update_position_func)
		self.synthesize_button.clicked.connect(self.synthesize_text)

	def sound_btn_func(self):
		if self.player.isMuted():
			self.player.setMuted(False)
			self.sound_btn.setIcon(QIcon("images/sound_on"))
		else:
			self.player.setMuted(True)
			self.sound_btn.setIcon(QIcon("images/sound_off"))

	def play_pause_btn_func(self):
		if self.player.state() == 1:
			self.player.pause()
			self.play_pause_btn.setIcon(QIcon("images/play.png"))
		else:
			self.player.play()
			self.play_pause_btn.setIcon(QIcon("images/pause.png"))

	def volume_slider_func(self, value):
		self.player.setVolume(value)
		if value == 0:
			self.sound_btn.setIcon(QIcon("images/sound_off.png"))
		else:
			self.sound_btn.setIcon(QIcon("images/sound_on.png"))

	def get_duration_func(self, d):
		self.progress_slider.setRange(0, d)
		self.progress_slider.setEnabled(True)
		self.get_time_func(d)

	def get_time_func(self, d):
		seconds = int(d / 1000)
		minutes = int(seconds / 60)
		seconds -= minutes * 60
		if minutes == 0 and seconds == 0:
			self.time_label.setText("--/--")
			self.play_pause_btn.setIcon(QIcon("images/play.png"))
		else:
			self.time_label.setText("{}:{}".format(minutes, seconds))

	def get_position_func(self, p):
		self.progress_slider.setValue(p)

	def update_position_func(self, v):
		self.player.setPosition(v)
		d = self.progress_slider.maximum() - v
		self.get_time_func(d)

	def synthesize_text(self):
		text = self.text_edit.toPlainText()
		if text == "":
			self.status_bar.showMessage("Please enter some text to synthesize.")
		else:
			self.status_bar.showMessage("Synthesizing ...")
			model_name = self.checkpoint_combo.currentText()
			audio_path, diacritized_text = self.synthesizer.synthesize(text, model_name)
			if diacritized_text is not None:
				self.text_edit.setText(diacritized_text)
			self.status_bar.showMessage("Synthesized audio saved to: {}".format(audio_path))
			self.play_audio(audio_path)

	def play_audio(self, audio_path):
		url = QUrl.fromLocalFile(audio_path)
		content = QMediaContent(url)
		self.player.setMedia(content)
		self.player.play()
		self.play_pause_btn.setIcon(QIcon("images/pause.png"))

	def closeEvent(self, event):
		self.player.stop()
		event.accept()
