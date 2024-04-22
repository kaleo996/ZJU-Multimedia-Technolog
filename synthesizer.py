from transformers import VitsModel, VitsTokenizer
import mishkal.tashkeel
# from unikud.framework import Unikud
import torch
import torchaudio
import time


class Synthesizer:
	def __init__(self):
		# create model only when needed
		self.abjad_vits_ara_vocalizer = None
		self.abjad_vits_ara_tokenizer = None
		self.abjad_vits_ara_model = None
	
		self.abjad_vits_heb_vocalizer = None
		self.abjad_vits_heb_tokenizer = None
		self.abjad_vits_heb_model = None

		self.mms_tts_ara_tokenizer = None
		self.mms_tts_ara_model = None

		self.mms_tts_heb_tokenizer = None
		self.mms_tts_heb_model = None

	def synthesize(self, text, model_name):
		file_name = time.strftime("%y-%m-%d-%H-%M-%S.wav", time.localtime())
		file_path = "output/" + file_name

		diacritized_text = None

		# init model
		if model_name == " Abjad-VITS-ara":
			if self.abjad_vits_ara_tokenizer is None:
				self.abjad_vits_ara_vocalizer = mishkal.tashkeel.TashkeelClass()
				self.abjad_vits_ara_tokenizer = VitsTokenizer.from_pretrained("ckpt/abjad-vits-ara")
				self.abjad_vits_ara_model = VitsModel.from_pretrained("ckpt/abjad-vits-ara")
			diacritized_text = text = self.abjad_vits_ara_vocalizer.tashkeel(text)
			tokenizer = self.abjad_vits_ara_tokenizer
			model = self.abjad_vits_ara_model
		elif model_name == " Abjad-VITS-heb":
			if self.abjad_vits_heb_tokenizer is None:
				# self.abjad_vits_heb_vocalizer = Unikud()
				self.abjad_vits_heb_tokenizer = VitsTokenizer.from_pretrained("ckpt/abjad-vits-heb")
				self.abjad_vits_heb_model = VitsModel.from_pretrained("ckpt/abjad-vits-heb")
			diacritized_text = None
			# diacritized_text = text = self.abjad_vits_heb_vocalizer(text)
			tokenizer = self.abjad_vits_heb_tokenizer
			model = self.abjad_vits_heb_model
		elif model_name == " MMS-TTS-ara":
			if self.mms_tts_ara_tokenizer is None:
				self.mms_tts_ara_tokenizer = VitsTokenizer.from_pretrained("ckpt/mms-tts-ara")
				self.mms_tts_ara_model = VitsModel.from_pretrained("ckpt/mms-tts-ara")
			diacritized_text = None
			tokenizer = self.mms_tts_ara_tokenizer
			model = self.mms_tts_ara_model
		elif model_name == " MMS-TTS-heb":
			if self.mms_tts_heb_tokenizer is None:
				self.mms_tts_heb_tokenizer = VitsTokenizer.from_pretrained("ckpt/mms-tts-heb")
				self.mms_tts_heb_model = VitsModel.from_pretrained("ckpt/mms-tts-heb")
			diacritized_text = None
			tokenizer = self.mms_tts_heb_tokenizer
			model = self.mms_tts_heb_model

		# synthesize and save result
		inputs = tokenizer(text, return_tensors="pt")
		with torch.no_grad():
			waveform = model(**inputs).waveform
		torchaudio.save(file_path, waveform, model.config.sampling_rate)

		return file_path, diacritized_text