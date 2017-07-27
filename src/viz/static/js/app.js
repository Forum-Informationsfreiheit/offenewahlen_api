"use strict";

class CountDown {
	constructor (countdown_target, target_ids) {
		this.countdown_target = countdown_target;
		this.target_selectors = {};
		this.countdown_data = {};
		this.setup(target_ids);
		this.run_countdown();
	}

	setup (target_ids) {
		for (let key in target_ids) {
			this.target_selectors[key] = $('#' + target_ids[key]);
		}
	}

	run_countdown () {
		setInterval(this.update_timer.bind(this), 1000);
	}

	update_timer () {
		this.update_countdown_data();

		for (let key in this.target_selectors) {
			this.target_selectors[key].html(this.countdown_data[key]);
		}
	}

	update_countdown_data () {
		let seconds_to_publish = this.get_seconds_to_publish();
		let days = Math.floor(seconds_to_publish / 86400);
		seconds_to_publish = seconds_to_publish - days * 86400;
		let hours = Math.floor(seconds_to_publish / 3600);
		seconds_to_publish = seconds_to_publish - hours * 3600;
		let minutes = Math.floor(seconds_to_publish / 60);
		seconds_to_publish = Math.round(seconds_to_publish - minutes * 60);

		this.countdown_data = {
			"days": days,
			"hours": hours,
			"minutes": minutes,
			"seconds": seconds_to_publish
		};
	}

	get_seconds_to_publish () {
		let publish_date_seconds =
			new Date(this.countdown_target).getTime() / 1000;
		let now_seconds = Date.now() / 1000;
		let seconds_to_release = publish_date_seconds - now_seconds;

		return seconds_to_release;
	}
}

let target_ids = {
	"days": "countdown-days",
	"hours": "countdown-hours",
	"minutes": "countdown-minutes",
	"seconds": "countdown-seconds"
};

let count = new CountDown("2017-10-15T17:00", target_ids);

$('#mce-EMAIL').on('focus', function () {
   	$(this).val("");
});

