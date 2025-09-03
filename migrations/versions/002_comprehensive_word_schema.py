"""Comprehensive word schema implementation

Revision ID: 002
Revises: 001
Create Date: 2024-01-01 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID, JSON


# revision identifiers, used by Alembic.
revision: str = '002'
down_revision: Union[str, None] = '001'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Drop the old words table
    op.drop_table('words')
    
    # Create comprehensive word schema
    op.create_table('words',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('lemma', sa.String(), nullable=False),
        sa.Column('lang', sa.String(), nullable=False),
        sa.Column('pos', sa.Enum('NOUN', 'VERB', 'ADJECTIVE', 'ADVERB', 'PRONOUN', 'PREPOSITION', 'CONJUNCTION', 'INTERJECTION', 'ARTICLE', 'DETERMINER', 'PARTICLE', 'OTHER', name='partofspeech'), nullable=False),
        sa.Column('pos_specific', sa.String(), nullable=True),
        sa.Column('defs', JSON(), nullable=False),
        sa.Column('synonyms', JSON(), nullable=True),
        sa.Column('examples', JSON(), nullable=True),
        sa.Column('freq_rank', sa.Integer(), nullable=True),
        sa.Column('cefr', sa.Enum('A1', 'A2', 'B1', 'B2', 'C1', 'C2', name='cefrlevel'), nullable=True),
        sa.Column('gender', sa.Enum('MASCULINE', 'FEMININE', 'NEUTER', name='gender'), nullable=True),
        sa.Column('plural', sa.String(), nullable=True),
        sa.Column('audio', sa.Text(), nullable=True),
        sa.Column('src', sa.String(), nullable=True),
        sa.Column('success_streak', sa.Integer(), nullable=True),
        sa.Column('last_reviewed_at', sa.DateTime(), nullable=True),
        sa.Column('next_review_at', sa.DateTime(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_words_id'), 'words', ['id'], unique=False)
    op.create_index(op.f('ix_words_lemma'), 'words', ['lemma'], unique=False)
    op.create_index(op.f('ix_words_lang'), 'words', ['lang'], unique=False)


def downgrade() -> None:
    # Drop the comprehensive words table
    op.drop_index(op.f('ix_words_lang'), table_name='words')
    op.drop_index(op.f('ix_words_lemma'), table_name='words')
    op.drop_index(op.f('ix_words_id'), table_name='words')
    op.drop_table('words')
    
    # Recreate the old simple words table
    op.create_table('words',
        sa.Column('id', UUID(as_uuid=True), nullable=False),
        sa.Column('word', sa.String(), nullable=False),
        sa.Column('definition', sa.String(), nullable=False),
        sa.Column('part_of_speech', sa.Enum('NOUN', 'VERB', 'ADJECTIVE', 'ADVERB', 'PRONOUN', 'PREPOSITION', 'CONJUNCTION', 'INTERJECTION', 'ARTICLE', 'OTHER', name='partofspeech'), nullable=False),
        sa.Column('difficulty', sa.Enum('BEGINNER', 'INTERMEDIATE', 'ADVANCED', name='difficultylevel'), nullable=False),
        sa.Column('language', sa.String(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('word', 'language', name='uq_word_language')
    )
    op.create_index(op.f('ix_words_id'), 'words', ['id'], unique=False)
    op.create_index(op.f('ix_words_word'), 'words', ['word'], unique=False)