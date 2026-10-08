"""Pentagram Research Milestone: an interactive PySide6 desktop prototype."""

import sys

from PySide6.QtCore import Qt
from PySide6.QtGui import QColor
from PySide6.QtWidgets import (
    QApplication,
    QCheckBox,
    QFormLayout,
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QPushButton,
    QSpinBox,
    QStackedWidget,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from simulation import SimulationResult, run_mock_simulation


class PentagramWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Pentagram Research Prototype")
        self.setMinimumSize(900, 650)
        self._build_ui()
        self._apply_style()

    def _build_ui(self) -> None:
        self.pages = QStackedWidget()
        self.pages.addWidget(self._create_configuration_page())
        self.pages.addWidget(self._create_results_page())
        self.setCentralWidget(self.pages)

    def _create_header(self, subtitle: str) -> QVBoxLayout:
        heading = QLabel("Pentagram")
        heading.setObjectName("heading")
        description = QLabel(subtitle)
        description.setObjectName("subtitle")
        layout = QVBoxLayout()
        layout.setSpacing(2)
        layout.addWidget(heading)
        layout.addWidget(description)
        return layout

    def _create_configuration_page(self) -> QWidget:
        page = QWidget()
        outer = QVBoxLayout(page)
        outer.setContentsMargins(60, 45, 60, 45)
        outer.setSpacing(26)
        outer.addLayout(self._create_header("Configure a local, simulated federated-learning experiment."))

        card = QFrame()
        card.setObjectName("card")
        form = QFormLayout(card)
        form.setContentsMargins(32, 28, 32, 28)
        form.setVerticalSpacing(18)
        form.setHorizontalSpacing(24)

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("e.g., Ashwin")
        self.hospital_input = QSpinBox()
        self.hospital_input.setRange(3, 5)
        self.hospital_input.setValue(4)
        self.round_input = QSpinBox()
        self.round_input.setRange(1, 10)
        self.round_input.setValue(5)
        self.dropout_input = QCheckBox("Simulate one hospital dropout during the run")

        form.addRow("Display name:", self.name_input)
        form.addRow("Virtual hospitals:", self.hospital_input)
        form.addRow("Training rounds:", self.round_input)
        form.addRow("Availability event:", self.dropout_input)
        outer.addWidget(card)

        scope_note = QLabel(
            "Prototype scope: deterministic mock metrics only. No PHI, cloud services, "
            "networking, or real model training is used."
        )
        scope_note.setWordWrap(True)
        scope_note.setObjectName("note")
        outer.addWidget(scope_note)

        run_button = QPushButton("Run Simulation")
        run_button.setObjectName("primaryButton")
        run_button.clicked.connect(self.run_simulation)
        outer.addWidget(run_button, alignment=Qt.AlignmentFlag.AlignRight)
        outer.addStretch()
        return page

    def _create_results_page(self) -> QWidget:
        page = QWidget()
        outer = QVBoxLayout(page)
        outer.setContentsMargins(60, 45, 60, 45)
        outer.setSpacing(20)
        outer.addLayout(self._create_header("Mock simulation results"))

        self.summary_label = QLabel()
        self.summary_label.setObjectName("summary")
        self.summary_label.setWordWrap(True)
        outer.addWidget(self.summary_label)

        metrics = QGridLayout()
        self.accuracy_value = self._metric_card(metrics, 0, "Final federated accuracy")
        self.loss_value = self._metric_card(metrics, 1, "Final federated loss")
        self.rounds_value = self._metric_card(metrics, 2, "Completed rounds")
        outer.addLayout(metrics)

        tables = QHBoxLayout()
        self.hospital_table = QTableWidget(0, 2)
        self.hospital_table.setHorizontalHeaderLabels(["Virtual hospital", "Status"])
        self.hospital_table.horizontalHeader().setStretchLastSection(True)
        self.round_table = QTableWidget(0, 3)
        self.round_table.setHorizontalHeaderLabels(["Round", "Accuracy", "Loss"])
        self.round_table.horizontalHeader().setStretchLastSection(True)

        for title, table in (("Hospital participation", self.hospital_table), ("Round-by-round metrics", self.round_table)):
            section = QVBoxLayout()
            label = QLabel(title)
            label.setObjectName("sectionTitle")
            section.addWidget(label)
            section.addWidget(table)
            tables.addLayout(section)
        outer.addLayout(tables)

        new_run_button = QPushButton("Configure Another Run")
        new_run_button.clicked.connect(lambda: self.pages.setCurrentIndex(0))
        outer.addWidget(new_run_button, alignment=Qt.AlignmentFlag.AlignRight)
        return page

    def _metric_card(self, layout: QGridLayout, column: int, label_text: str) -> QLabel:
        card = QFrame()
        card.setObjectName("metricCard")
        card_layout = QVBoxLayout(card)
        label = QLabel(label_text)
        label.setObjectName("metricLabel")
        value = QLabel("—")
        value.setObjectName("metricValue")
        card_layout.addWidget(label)
        card_layout.addWidget(value)
        layout.addWidget(card, 0, column)
        return value

    def run_simulation(self) -> None:
        name = self.name_input.text().strip() or "Local user"
        result = run_mock_simulation(
            name,
            self.hospital_input.value(),
            self.round_input.value(),
            self.dropout_input.isChecked(),
        )
        self._show_result(result)
        self.pages.setCurrentIndex(1)

    def _show_result(self, result: SimulationResult) -> None:
        self.summary_label.setText(
            f"<b>{result.display_name}</b>'s run used {result.hospital_count} virtual hospitals. "
            "Only simulated model updates are represented in this prototype."
        )
        self.accuracy_value.setText(f"{result.final_accuracy:.1%}")
        self.loss_value.setText(f"{result.final_loss:.3f}")
        self.rounds_value.setText(str(len(result.rounds)))

        self.hospital_table.setRowCount(len(result.hospital_statuses))
        for row, (hospital, status) in enumerate(result.hospital_statuses):
            self.hospital_table.setItem(row, 0, QTableWidgetItem(hospital))
            status_item = QTableWidgetItem(status)
            status_item.setForeground(QColor("#b42318") if "Dropped" in status else QColor("#067647"))
            self.hospital_table.setItem(row, 1, status_item)

        self.round_table.setRowCount(len(result.rounds))
        for row, round_result in enumerate(result.rounds):
            self.round_table.setItem(row, 0, QTableWidgetItem(str(round_result.round_number)))
            self.round_table.setItem(row, 1, QTableWidgetItem(f"{round_result.accuracy:.1%}"))
            self.round_table.setItem(row, 2, QTableWidgetItem(f"{round_result.loss:.3f}"))

    def _apply_style(self) -> None:
        self.setStyleSheet("""
            QMainWindow { background: #f5fbff; color: #17324d; }
            QLabel, QCheckBox, QTableWidget, QTableWidget::item { color: #17324d; }
            #heading { color: #0b5d87; font-size: 30px; font-weight: 700; }
            #subtitle { color: #547083; font-size: 15px; }
            #card, #metricCard { background: white; border: 1px solid #cce5ef; border-radius: 10px; }
            #metricCard { min-width: 175px; padding: 8px; }
            #metricLabel { color: #547083; font-size: 12px; }
            #metricValue { color: #0b5d87; font-size: 25px; font-weight: 700; }
            #summary { background: #e8f7f0; border-radius: 8px; padding: 12px; color: #155b43; }
            #sectionTitle { color: #0b5d87; font-size: 16px; font-weight: 700; }
            #note { color: #547083; }
            QLineEdit, QSpinBox { min-height: 30px; padding: 3px 8px; border: 1px solid #aacddc; border-radius: 6px; background: #ffffff; color: #17324d; }
            QLineEdit::placeholder { color: #6d8493; }
            QPushButton { min-height: 34px; padding: 4px 16px; border: 1px solid #0b5d87; border-radius: 7px; background: white; color: #0b5d87; font-weight: 600; }
            QPushButton:hover { background: #e4f3f8; }
            #primaryButton { background: #0b7a75; color: white; border-color: #0b7a75; }
            #primaryButton:hover { background: #086661; }
            QTableWidget { background: white; color: #17324d; border: 1px solid #cce5ef; border-radius: 8px; gridline-color: #e3eef3; }
            QHeaderView::section { background: #e4f3f8; padding: 7px; border: none; color: #17324d; font-weight: 600; }
        """)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PentagramWindow()
    window.show()
    sys.exit(app.exec())

